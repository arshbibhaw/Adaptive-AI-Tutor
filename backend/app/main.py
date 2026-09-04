"""
Main application entrypoint.

FastAPI application with CORS, routers, and database lifecycle management.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.core.config import settings
from backend.app.core.database import init_db

# Import all models so SQLAlchemy registers them before table creation
import backend.app.models  # noqa: F401

# Import routers
from backend.app.api.documents import router as documents_router
from backend.app.api.sessions import router as sessions_router
from backend.app.api.assessment import router as assessment_router
from backend.app.api.video import router as video_router
from backend.app.api.progress import router as progress_router
from backend.app.api.learner import router as learner_router
from backend.app.api.auth import router as auth_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown lifecycle."""
    logger.info("Starting AI Teacher API...")
    await init_db()
    logger.info("Database tables created.")
    yield
    logger.info("Shutting down AI Teacher API.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Adaptive AI Teacher — Personalized, Intelligent Teaching Companion",
    lifespan=lifespan,
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(documents_router, prefix="/api/documents", tags=["Documents"])
app.include_router(sessions_router, prefix="/api/sessions", tags=["Sessions"])
app.include_router(assessment_router, prefix="/api/assessment", tags=["Assessment"])
app.include_router(video_router, prefix="/api/video", tags=["Video"])
app.include_router(progress_router, prefix="/api/progress", tags=["Progress"])
app.include_router(learner_router, prefix="/api/learner", tags=["Learner"])


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.APP_VERSION}


@app.get("/api/health", tags=["Health"])
async def health_check():
    """Detailed health check."""
    return {
        "status": "ok",
        "database": "connected",
        "llm_configured": bool(settings.LLM_API_KEY),
        "tts_configured": bool(settings.TTS_API_KEY),
        "avatar_configured": bool(settings.AVATAR_API_KEY),
    }
