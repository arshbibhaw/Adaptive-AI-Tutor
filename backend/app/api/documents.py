"""
Documents API endpoints.

POST /documents/upload — Upload an educational document.
POST /documents/{id}/index — Index a document for RAG.
GET  /documents/{id}/outline — Get the document's structural outline.
"""

import logging
import os

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.dependencies import get_current_user_id
from backend.app.models.document import Document
from backend.app.schemas.document import DocumentUploadResponse, DocumentOutlineResponse
from backend.app.services.rag.ingestion import validate_file, save_upload, ingest_document

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Upload an educational document (PDF, DOCX, PPTX, TXT)."""
    # Validate
    file_content = await file.read()
    file_size = len(file_content)
    filename = file.filename or "unknown"
    file_type = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""

    error = validate_file(filename, file_size)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    # Save file
    doc_id, file_path = await save_upload(file_content, filename)

    # Create DB record
    doc = Document(
        id=doc_id,
        user_id=user_id,
        filename=filename,
        file_type=file_type,
        file_size=file_size,
        file_path=file_path,
        status="uploaded",
    )
    db.add(doc)
    await db.flush()

    logger.info("Document uploaded: %s (id=%s, type=%s, size=%d)", filename, doc_id, file_type, file_size)

    return DocumentUploadResponse(
        id=doc_id,
        filename=filename,
        file_type=file_type,
        file_size=file_size,
        status="uploaded",
    )


@router.post("/{document_id}/index", response_model=DocumentOutlineResponse)
async def index_document(
    document_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Index a document for RAG retrieval."""
    # Fetch document
    result = await db.execute(
        select(Document).where(Document.id == document_id, Document.user_id == user_id)
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    if doc.status == "indexed":
        return DocumentOutlineResponse(
            id=doc.id, filename=doc.filename, outline=doc.outline,
            status=doc.status, chunk_count=doc.chunk_count,
        )

    # Update status
    doc.status = "processing"
    await db.flush()

    try:
        result_data = await ingest_document(doc.id, doc.file_path, doc.file_type)
        doc.outline = result_data["outline"]
        doc.chunk_count = result_data["chunk_count"]
        doc.status = "indexed"
        await db.flush()

        logger.info("Document indexed: %s (chunks=%d)", doc.id, doc.chunk_count)
    except Exception as e:
        doc.status = "failed"
        await db.flush()
        logger.error("Document indexing failed: %s — %s", doc.id, e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Indexing failed: {str(e)}",
        )

    return DocumentOutlineResponse(
        id=doc.id, filename=doc.filename, outline=doc.outline,
        status=doc.status, chunk_count=doc.chunk_count,
    )


@router.get("/{document_id}/outline", response_model=DocumentOutlineResponse)
async def get_outline(
    document_id: str,
    user_id: str = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
):
    """Get the structural outline of an indexed document."""
    result = await db.execute(
        select(Document).where(Document.id == document_id, Document.user_id == user_id)
    )
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found.")

    return DocumentOutlineResponse(
        id=doc.id, filename=doc.filename, outline=doc.outline,
        status=doc.status, chunk_count=doc.chunk_count,
    )
