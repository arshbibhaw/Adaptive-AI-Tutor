"""
Core application configuration.

Loads all settings from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from .env file."""

    # --- Application ---
    APP_NAME: str = "AI Teacher"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # --- Database (PostgreSQL / Supabase) ---
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/ai_teacher"

    # --- Authentication ---
    AUTH_SECRET: str = "change-this-to-a-secure-random-string"
    AUTH_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- File Storage ---
    UPLOAD_DIR: str = "./data/uploads"
    PROCESSED_DIR: str = "./data/processed"

    # --- CORS ---
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    # ============================================================
    # PLACEHOLDER — LLM Provider (to be configured later)
    # ============================================================
    # TODO: Configure when LLM provider is selected.
    LLM_PROVIDER: str = ""
    LLM_API_KEY: str = ""
    LLM_MODEL: str = ""

    # ============================================================
    # PLACEHOLDER — Embedding Provider (to be configured later)
    # ============================================================
    # TODO: Configure when embedding provider is selected.
    EMBEDDING_API_KEY: str = ""
    EMBEDDING_MODEL: str = ""

    # ============================================================
    # PLACEHOLDER — Vector Database (to be configured later)
    # ============================================================
    # TODO: Configure when vector DB is selected.
    VECTOR_DB_URL: str = ""
    VECTOR_DB_KEY: str = ""

    # ============================================================
    # PLACEHOLDER — TTS Provider (to be configured later)
    # ============================================================
    # TODO: Configure when TTS provider is selected (e.g., ElevenLabs).
    TTS_PROVIDER: str = ""
    TTS_API_KEY: str = ""
    TTS_VOICE_ID: str = ""

    # ============================================================
    # PLACEHOLDER — Avatar Provider (to be configured later)
    # ============================================================
    # TODO: Configure when avatar provider is selected (e.g., HeyGen, D-ID).
    AVATAR_PROVIDER: str = ""
    AVATAR_API_KEY: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
