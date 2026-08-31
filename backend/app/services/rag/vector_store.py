"""
RAG vector store service.

Manages storage and retrieval of embedded document chunks.

============================================================
PLACEHOLDER — Vector database not yet configured.
============================================================
TODO: When the vector DB is selected, replace the in-memory
store with actual vector DB integration.
Candidate providers:
  - ChromaDB (local, zero-config)
  - Pinecone
  - Weaviate
  - Supabase pgvector
============================================================
"""

import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

# In-memory store for pipeline testing
# Structure: {document_id: [{"chunk_id": ..., "text": ..., "embedding": [...], ...}]}
_store: dict[str, list[dict]] = defaultdict(list)


async def store_chunks(document_id: str, chunks: list[dict]) -> None:
    """
    Store embedded chunks for a document.

    ============================================================
    PLACEHOLDER: Uses an in-memory dict. Replace with vector DB.
    ============================================================
    """
    logger.warning(
        "PLACEHOLDER: Using in-memory vector store. Configure VECTOR_DB_URL for persistence."
    )
    _store[document_id] = chunks
    logger.info("Stored %d chunks for document %s in memory.", len(chunks), document_id)


async def query_chunks(
    document_id: str,
    query_embedding: list[float],
    top_k: int = 5,
) -> list[dict]:
    """
    Query the vector store for the most similar chunks.

    ============================================================
    PLACEHOLDER: Uses cosine similarity on in-memory store.
    Replace with vector DB query when configured.
    ============================================================
    """
    chunks = _store.get(document_id, [])
    if not chunks:
        logger.warning("No chunks found for document %s.", document_id)
        return []

    # Compute cosine similarity
    scored = []
    for chunk in chunks:
        chunk_emb = chunk.get("embedding", [])
        if chunk_emb:
            score = _cosine_similarity(query_embedding, chunk_emb)
            scored.append({**chunk, "score": score})

    # Sort by score descending
    scored.sort(key=lambda x: x.get("score", 0), reverse=True)

    return scored[:top_k]


async def delete_chunks(document_id: str) -> None:
    """Delete all chunks for a document."""
    if document_id in _store:
        del _store[document_id]
        logger.info("Deleted chunks for document %s.", document_id)


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
