"""
RAG chunking service.

Splits structured document content into chunks with metadata preservation.
Each chunk carries: document_id, page, chapter, section, chunk_id.
"""

import logging
import uuid

logger = logging.getLogger(__name__)

DEFAULT_CHUNK_SIZE = 500  # characters
DEFAULT_CHUNK_OVERLAP = 100  # characters


def chunk_document(
    document_id: str,
    structured: dict,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> list[dict]:
    """
    Chunk a structured document into smaller pieces with metadata.

    Returns a list of chunk dicts:
    [
        {
            "chunk_id": str,
            "document_id": str,
            "text": str,
            "page": int | None,
            "chapter": str,
            "section": str,
        },
        ...
    ]
    """
    chunks = []

    for section in structured.get("sections", []):
        content = section.get("content", "")
        if not content.strip():
            continue

        section_chunks = _split_text(content, chunk_size, chunk_overlap)

        for chunk_text in section_chunks:
            if not chunk_text.strip():
                continue
            chunks.append({
                "chunk_id": str(uuid.uuid4()),
                "document_id": document_id,
                "text": chunk_text.strip(),
                "page": section.get("page"),
                "chapter": section.get("heading", ""),
                "section": section.get("type", "content"),
            })

    logger.info("Chunked document %s into %d chunks.", document_id, len(chunks))
    return chunks


def _split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    Split text into overlapping chunks, trying to break at sentence boundaries.
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at a sentence boundary
        if end < len(text):
            # Look for sentence-ending punctuation near the chunk boundary
            break_point = _find_sentence_break(text, start, end)
            if break_point > start:
                end = break_point

        chunks.append(text[start:end])

        # Move forward by (chunk_size - overlap)
        start = end - overlap
        if start >= len(text):
            break

    return chunks


def _find_sentence_break(text: str, start: int, end: int) -> int:
    """Find the best sentence break point near the end position."""
    # Search backwards from end for sentence-ending punctuation
    search_start = max(start, end - 100)
    for i in range(end, search_start, -1):
        if i < len(text) and text[i] in ".!?\n":
            return i + 1
    return end
