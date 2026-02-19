"""
Application configuration using Pydantic Settings.
Reads from .env file and environment variables.
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration for the Smart Document Insights platform."""

    # --- Application ---
    app_name: str = "Smart Document Insights"
    app_env: str = "development"
    debug: bool = True
    secret_key: str = "change-me-to-a-random-secret-key"

    # --- Database ---
    database_url: str = "sqlite+aiosqlite:///./data/app.db"

    # --- OpenAI / LLM ---
    openai_api_key: str = ""
    openai_model: str = "gpt-3.5-turbo"
    openai_api_base: str | None = None
    llm_max_retries: int = 2
    llm_timeout: int = 60

    # --- LLM Cache ---
    llm_cache_max_size: int = 256
    llm_cache_ttl: int = 3600  # seconds

    # --- Embeddings ---
    embedding_model: str = "text-embedding-3-small"
    use_local_embeddings: bool = False
    embedding_cache_size: int = 512

    # --- Vector Store ---
    faiss_index_path: str = "./data/faiss_index"

    # --- Redis ---
    redis_url: str = "redis://localhost:6379/0"

    # --- File Upload ---
    max_file_size_mb: int = 50
    upload_dir: str = "./data/uploads"
    allowed_extensions: str = "pdf,docx,txt"

    # --- Rate Limiting ---
    rate_limit_per_minute: int = 60

    # --- CORS ---
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # --- API ---
    api_version: str = "v1"

    @property
    def max_file_size_bytes(self) -> int:
        return self.max_file_size_mb * 1024 * 1024

    @property
    def allowed_extensions_list(self) -> list[str]:
        return [ext.strip() for ext in self.allowed_extensions.split(",")]

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def is_llm_configured(self) -> bool:
        """Check if an LLM API key is configured."""
        return bool(
            self.openai_api_key
            and self.openai_api_key != "sk-your-openai-api-key-here"
            and len(self.openai_api_key) > 10
        )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Cached settings singleton."""
    return Settings()
