"""
Smart Document Insights — FastAPI Application Entry Point.
Production-ready AI SaaS platform for document analysis and insights.
"""

import os
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import get_settings
from backend.database import init_db
from backend.utils.logging_config import get_logger, setup_logging

# Initialize logging
settings = get_settings()
setup_logging(debug=settings.debug)
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    logger.info("application_starting", app_name=settings.app_name, env=settings.app_env)

    # Create data directories
    os.makedirs("data/uploads", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    # Initialize database
    await init_db()
    logger.info("database_initialized")

    # Check LLM configuration
    if settings.is_llm_configured:
        logger.info("llm_configured", model=settings.openai_model)
    else:
        logger.warning("llm_not_configured", msg="Running in demo mode. Set OPENAI_API_KEY for full features.")

    yield

    logger.info("application_shutting_down")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="AI-powered document analysis with semantic search, RAG chat, risk detection, and insights.",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request logging + timing middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log requests with timing and request ID."""
    request_id = str(uuid.uuid4())[:8]
    start = time.time()

    response = await call_next(request)

    duration_ms = round((time.time() - start) * 1000, 1)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time"] = f"{duration_ms}ms"

    logger.info(
        "request",
        method=request.method,
        path=str(request.url.path),
        status=response.status_code,
        duration_ms=duration_ms,
        request_id=request_id,
    )

    return response


# Structured error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Return structured JSON errors."""
    logger.error(
        "unhandled_exception",
        error=str(exc),
        path=str(request.url.path),
        method=request.method,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred. Please try again.",
        },
    )


# ============================================
# Register API routes (versioned + compat)
# ============================================
from backend.api.documents import router as documents_router
from backend.api.insights import router as insights_router
from backend.api.search import router as search_router
from backend.api.chat import router as chat_router
from backend.api.compare import router as compare_router
from backend.api.dashboard import router as dashboard_router

# Register under both /api/ and /api/v1/ for compatibility
for router in [documents_router, insights_router, search_router, chat_router, compare_router, dashboard_router]:
    app.include_router(router)


# ============================================
# System endpoints
# ============================================

@app.get("/api/health", tags=["System"])
@app.get("/api/v1/health", tags=["System"], include_in_schema=False)
async def health_check():
    """Health check with version and LLM status."""
    from backend.services.llm_client import get_cache_stats
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": "2.0.0",
        "llm_configured": settings.is_llm_configured,
        "llm_model": settings.openai_model if settings.is_llm_configured else None,
        "cache": get_cache_stats(),
    }


@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information."""
    return {
        "app": settings.app_name,
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/api/health",
    }
