"""
RAG ingestion service.

Orchestrates the full document processing pipeline:
file validation → extraction → cleaning → chunking → embedding → vector store.
"""

import logging
import os
import uuid

from backend.app.core.config import settings
from backend.app.services.rag.extraction import extract_text
from backend.app.services.rag.cleaning import clean_and_structure
from backend.app.services.rag.chunking import chunk_document
from backend.app.services.rag.embeddings import generate_embeddings
from backend.app.services.rag.vector_store import store_chunks

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"pdf", "docx", "pptx", "txt", "md"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def validate_file(filename: str, file_size: int) -> str | None:
    """
    Validate file type and size.

    Returns an error message string if invalid, or None if valid.
    """
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        return f"Unsupported file type: .{ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    if file_size > MAX_FILE_SIZE:
        return f"File too large: {file_size} bytes. Max: {MAX_FILE_SIZE} bytes."
    return None


async def save_upload(file_content: bytes, filename: str) -> tuple[str, str]:
    """
    Save an uploaded file to the uploads directory.

    Returns (document_id, file_path).
    """
    document_id = str(uuid.uuid4())
    ext = filename.rsplit(".", 1)[-1].lower()
    safe_filename = f"{document_id}.{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(file_content)

    logger.info("Saved upload: %s -> %s", filename, file_path)
    return document_id, file_path


async def ingest_document(
    document_id: str,
    file_path: str,
    file_type: str,
) -> dict:
    """
    Run the full ingestion pipeline for a document.

    Returns the document outline and chunk count.
    """
    logger.info("Starting ingestion for document %s (%s)", document_id, file_type)

    # Step 1: Extract text
    raw_pages = extract_text(file_path, file_type)
    logger.info("Extracted %d pages/sections from document.", len(raw_pages))

    # Step 2: Clean and detect structure
    structured = clean_and_structure(raw_pages)
    logger.info("Cleaned and structured document: %d sections.", len(structured.get("sections", [])))

    # Step 3: Chunk
    chunks = chunk_document(document_id, structured)
    logger.info("Created %d chunks.", len(chunks))

    # Step 4: Generate embeddings
    embedded_chunks = await generate_embeddings(chunks)
    logger.info("Generated embeddings for %d chunks.", len(embedded_chunks))

    # Step 5: Store in vector DB
    await store_chunks(document_id, embedded_chunks)
    logger.info("Stored %d chunks in vector DB.", len(embedded_chunks))

    outline = {
        "title": structured.get("title", "Untitled"),
        "sections": [
            {"heading": s.get("heading", ""), "page": s.get("page")}
            for s in structured.get("sections", [])
        ],
        "total_pages": len(raw_pages),
    }

    return {"outline": outline, "chunk_count": len(chunks)}
