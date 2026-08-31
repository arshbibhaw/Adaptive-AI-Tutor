"""
Document schemas.

Request/response models for document upload and retrieval operations.
"""

from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    """Response after uploading a document."""
    id: str
    filename: str
    file_type: str
    file_size: int
    status: str


class DocumentOutlineResponse(BaseModel):
    """Response containing the document's structural outline."""
    id: str
    filename: str
    outline: dict | None
    status: str
    chunk_count: int | None


class RetrievalChunk(BaseModel):
    """A single retrieved chunk from the vector store."""
    text: str
    page: int | None = None
    chapter: str | None = None
    section: str | None = None
    chunk_id: str | None = None
    score: float | None = None


class RetrievalRequest(BaseModel):
    """Request to search the vector store."""
    query: str
    document_id: str
    top_k: int = 5


class RetrievalResponse(BaseModel):
    """Response from vector store search."""
    query: str
    chunks: list[RetrievalChunk]
