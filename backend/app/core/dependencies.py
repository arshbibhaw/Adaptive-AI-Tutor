"""
FastAPI dependencies.

Shared dependency injection for database sessions, authentication, and settings.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import Settings, settings
from backend.app.core.database import get_db
from backend.app.core.security import decode_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def get_settings() -> Settings:
    """Return the application settings instance."""
    return settings


async def get_current_user_id(
    token: str | None = Depends(oauth2_scheme),
) -> str:
    """
    Extract and return the current user ID from the JWT token.

    Raises HTTPException 401 if the token is missing or invalid.
    """
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id: str | None = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload missing user ID",
        )
    return user_id


async def get_optional_user_id(
    token: str | None = Depends(oauth2_scheme),
) -> str | None:
    """
    Extract the current user ID if a token is present; return None otherwise.

    Does not raise an error for unauthenticated requests.
    """
    if token is None:
        return None
    payload = decode_access_token(token)
    if payload is None:
        return None
    return payload.get("sub")
