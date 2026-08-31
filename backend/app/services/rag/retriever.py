"""
RAG retriever service.

Performs semantic search over indexed documents and returns
ranked chunks with source metadata for grounding the Teacher Agent.
"""

import logging

from backend.app.services.rag.embeddings import generate_embeddings
from backend.app.services.rag.vector_store import query_chunks

logger = logging.getLogger(__name__)

DEFAULT_TOP_K = 5
MIN_SCORE_THRESHOLD = 0.1


async def retrieve(
    query: str,
    document_id: str,
    top_k: int = DEFAULT_TOP_K,
) -> list[dict]:
    """
    Retrieve the most relevant chunks for a query from a document.

    Returns a list of chunks with source metadata:
    [
        {
            "text": str,
            "page": int | None,
            "chapter": str,
            "section": str,
            "chunk_id": str,
            "score": float,
        },
        ...
    ]
    """
    logger.info("Retrieving for query='%s' from document=%s (top_k=%d)", query, document_id, top_k)

    # Generate embedding for the query
    query_chunk = [{"text": query}]
    embedded = await generate_embeddings(query_chunk)
    query_embedding = embedded[0].get("embedding", [])

    if not query_embedding:
        logger.error("Failed to generate query embedding.")
        return []

    # Query vector store
    results = await query_chunks(document_id, query_embedding, top_k=top_k)

    # Filter by minimum score threshold
    filtered = [
        {
            "text": r["text"],
            "page": r.get("page"),
            "chapter": r.get("chapter", ""),
            "section": r.get("section", ""),
            "chunk_id": r.get("chunk_id", ""),
            "score": r.get("score", 0.0),
        }
        for r in results
        if r.get("score", 0.0) >= MIN_SCORE_THRESHOLD
    ]

    if not filtered:
        logger.warning(
            "No relevant chunks found for query='%s' in document=%s. "
            "The system should NOT confidently invent an answer.",
            query,
            document_id,
        )

    logger.info("Retrieved %d chunks (filtered from %d).", len(filtered), len(results))
    return filtered
