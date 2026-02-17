"""
Embedding service with query caching for fast repeated lookups.
Uses SentenceTransformers for local embedding generation.
"""

import hashlib
from collections import OrderedDict
from threading import Lock

import numpy as np

from backend.config import get_settings
from backend.utils.logging_config import get_logger

logger = get_logger(__name__)

# Singleton model
_embedding_model = None

# Query embedding cache (LRU, thread-safe)
_cache_lock = Lock()
_query_cache: OrderedDict[str, np.ndarray] = OrderedDict()
_CACHE_MAX_SIZE = 512


def get_embedding_model():
    """Get or create the SentenceTransformer model (singleton, lazy-loaded)."""
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer

        settings = get_settings()
        logger.info("loading_embedding_model", model=settings.embedding_model)
        _embedding_model = SentenceTransformer(settings.embedding_model)
        logger.info("embedding_model_loaded", model=settings.embedding_model)

    return _embedding_model


def embed_texts(texts: list[str], batch_size: int = 64) -> np.ndarray:
    """
    Embed a batch of texts.
    
    Args:
        texts: List of strings to embed.
        batch_size: Encoding batch size.
    
    Returns:
        numpy array of shape (len(texts), embedding_dim).
    """
    model = get_embedding_model()

    logger.info("embedding_texts", count=len(texts), batch_size=batch_size)
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=False,
        normalize_embeddings=True,
    )

    logger.info("texts_embedded", shape=embeddings.shape)
    return embeddings


def embed_query(query: str) -> np.ndarray:
    """
    Embed a single query with LRU caching.
    Repeated identical queries hit the cache and skip re-encoding.
    
    Args:
        query: Query text.
    
    Returns:
        numpy array of shape (1, embedding_dim).
    """
    cache_key = hashlib.md5(query.encode()).hexdigest()

    # Check cache
    with _cache_lock:
        if cache_key in _query_cache:
            _query_cache.move_to_end(cache_key)
            logger.debug("embedding_cache_hit", query=query[:50])
            return _query_cache[cache_key]

    # Generate embedding
    model = get_embedding_model()
    embedding = model.encode(
        [query],
        normalize_embeddings=True,
    )

    # Store in cache
    with _cache_lock:
        _query_cache[cache_key] = embedding
        while len(_query_cache) > _CACHE_MAX_SIZE:
            _query_cache.popitem(last=False)

    return embedding


def get_embedding_dimension() -> int:
    """Get the dimensionality of the embedding model."""
    model = get_embedding_model()
    return model.get_sentence_embedding_dimension()


def get_cache_stats() -> dict:
    """Get embedding cache statistics."""
    with _cache_lock:
        return {
            "size": len(_query_cache),
            "max_size": _CACHE_MAX_SIZE,
        }
