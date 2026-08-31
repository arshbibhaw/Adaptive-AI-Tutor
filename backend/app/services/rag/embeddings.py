"""
RAG embeddings service.

Generates vector embeddings for document chunks.

============================================================
PLACEHOLDER — Embedding provider not yet configured.
============================================================
TODO: When the embedding provider is selected, replace the
placeholder implementation below with actual API calls.
Candidate providers:
  - OpenAI text-embedding-3-small
  - Google Gemini Embedding
  - HuggingFace sentence-transformers (local)
============================================================
"""

import logging
import hashlib

logger = logging.getLogger(__name__)


async def generate_embeddings(chunks: list[dict]) -> list[dict]:
    """
    Generate embeddings for a list of document chunks.

    Each chunk dict must contain a 'text' field.
    Returns the same chunks with an added 'embedding' field.

    ============================================================
    PLACEHOLDER: Returns a deterministic dummy embedding vector.
    Replace with actual embedding API call when provider is configured.
    ============================================================
    """
    logger.warning(
        "PLACEHOLDER: Using dummy embeddings. Configure EMBEDDING_API_KEY for real embeddings."
    )

    embedded_chunks = []
    for chunk in chunks:
        text = chunk.get("text", "")
        embedding = _placeholder_embedding(text)
        embedded_chunks.append({**chunk, "embedding": embedding})

    return embedded_chunks


def _placeholder_embedding(text: str, dimensions: int = 384) -> list[float]:
    """
    Generate a deterministic placeholder embedding from text.

    NOT suitable for real semantic search — only for pipeline testing.
    """
    text_hash = hashlib.sha256(text.encode()).digest()
    # Create a deterministic vector from the hash
    embedding = []
    for i in range(dimensions):
        byte_val = text_hash[i % len(text_hash)]
        embedding.append((byte_val / 255.0) - 0.5)
    return embedding
