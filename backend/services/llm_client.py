"""
LLM client with async support, retry logic, response caching, and streaming.
Supports OpenAI, OpenRouter, and any OpenAI-compatible endpoint.
"""

import hashlib
import time
from collections import OrderedDict
from threading import Lock
from typing import Generator

from backend.config import get_settings
from backend.utils.logging_config import get_logger

logger = get_logger(__name__)


# ============================================
# Response Cache (LRU, thread-safe)
# ============================================

class LLMCache:
    """Thread-safe LRU cache for LLM responses."""

    def __init__(self, max_size: int = 256, ttl_seconds: int = 3600):
        self._cache: OrderedDict[str, tuple[str, float]] = OrderedDict()
        self._max_size = max_size
        self._ttl = ttl_seconds
        self._lock = Lock()
        self._hits = 0
        self._misses = 0

    def _make_key(self, prompt: str) -> str:
        return hashlib.md5(prompt.encode()).hexdigest()

    def get(self, prompt: str) -> str | None:
        key = self._make_key(prompt)
        with self._lock:
            if key in self._cache:
                response, timestamp = self._cache[key]
                if time.time() - timestamp < self._ttl:
                    self._cache.move_to_end(key)
                    self._hits += 1
                    return response
                else:
                    del self._cache[key]
            self._misses += 1
            return None

    def put(self, prompt: str, response: str) -> None:
        key = self._make_key(prompt)
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = (response, time.time())
            while len(self._cache) > self._max_size:
                self._cache.popitem(last=False)

    @property
    def stats(self) -> dict:
        return {
            "size": len(self._cache),
            "max_size": self._max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": f"{self._hits / max(1, self._hits + self._misses) * 100:.1f}%",
        }


# Global cache instance
_cache = LLMCache(max_size=256, ttl_seconds=3600)


# ============================================
# LLM Client
# ============================================

def get_llm_response(
    prompt: str,
    *,
    use_cache: bool = True,
    temperature: float = 0.1,
    max_tokens: int = 2000,
    max_retries: int = 2,
) -> str:
    """
    Get a response from the LLM with caching and retry.
    
    Args:
        prompt: The prompt to send.
        use_cache: Whether to check/store in cache.
        temperature: LLM temperature.
        max_tokens: Max response tokens.
        max_retries: Number of retry attempts on failure.
    
    Returns:
        LLM response text.
    """
    settings = get_settings()

    if not settings.is_llm_configured:
        logger.warning("llm_not_configured")
        return _mock_llm_response(prompt)

    # Check cache
    if use_cache:
        cached = _cache.get(prompt)
        if cached is not None:
            logger.debug("llm_cache_hit")
            return cached

    # Build LLM
    response = None
    last_error = None

    for attempt in range(max_retries + 1):
        try:
            response = _call_llm(prompt, settings, temperature, max_tokens)
            break
        except Exception as e:
            last_error = e
            if attempt < max_retries:
                wait = 2 ** attempt
                logger.warning("llm_retry", attempt=attempt + 1, wait=wait, error=str(e))
                time.sleep(wait)
            else:
                logger.error("llm_call_failed", error=str(e), attempts=max_retries + 1)

    if response is None:
        logger.error("llm_all_retries_exhausted", error=str(last_error))
        return _mock_llm_response(prompt)

    # Cache successful response
    if use_cache:
        _cache.put(prompt, response)

    return response


def _call_llm(prompt: str, settings, temperature: float, max_tokens: int) -> str:
    """Make a single LLM API call."""
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage

    kwargs = {
        "model": settings.openai_model,
        "api_key": settings.openai_api_key,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if settings.openai_api_base:
        kwargs["base_url"] = settings.openai_api_base

    llm = ChatOpenAI(**kwargs)
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content


def get_llm_streaming(prompt: str, **kwargs) -> Generator[str, None, None]:
    """
    Stream LLM response token-by-token.
    
    Yields:
        Response text chunks.
    """
    settings = get_settings()

    if not settings.is_llm_configured:
        yield _mock_llm_response(prompt)
        return

    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage

    llm_kwargs = {
        "model": settings.openai_model,
        "api_key": settings.openai_api_key,
        "temperature": kwargs.get("temperature", 0.1),
        "max_tokens": kwargs.get("max_tokens", 2000),
        "streaming": True,
    }
    if settings.openai_api_base:
        llm_kwargs["base_url"] = settings.openai_api_base

    llm = ChatOpenAI(**llm_kwargs)

    try:
        for chunk in llm.stream([HumanMessage(content=prompt)]):
            if chunk.content:
                yield chunk.content
    except Exception as e:
        logger.error("llm_stream_failed", error=str(e))
        yield _mock_llm_response(prompt)


def get_cache_stats() -> dict:
    """Get LLM cache statistics."""
    return _cache.stats


# ============================================
# Mock responses (fallback)
# ============================================

def _mock_llm_response(prompt: str) -> str:
    """Generate a mock response when no LLM is configured."""
    lower = prompt.lower()

    if "summarize" in lower or "summary" in lower:
        return '{"executive_summary": "Configure an LLM API key for real summaries.", "section_summaries": [], "bullet_highlights": ["Document processed successfully", "Set OPENAI_API_KEY for AI analysis"], "key_takeaways": ["Full AI analysis requires an API key"]}'

    if "risk" in lower:
        return '{"overall_risk_score": "Unknown", "risk_items": [], "total_risks": 0}'

    if "compare" in lower or "comparison" in lower:
        return '{"summary": "Configure an LLM API key for document comparison.", "similarities": [], "differences": []}'

    if "extract" in lower:
        return '{"main_topics": ["Document processed"], "key_points": ["Set OPENAI_API_KEY for extraction"], "action_items": [], "references": []}'

    return "This is a placeholder response. Configure OPENAI_API_KEY for real AI-powered analysis."
