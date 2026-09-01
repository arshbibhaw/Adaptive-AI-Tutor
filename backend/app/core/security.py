"""
Security configuration.

JWT token creation/verification and password hashing.
"""

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
import bcrypt

from backend.app.core.config import settings

def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hash."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), 
        hashed_password.encode("utf-8")
    )


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.AUTH_SECRET, algorithm=settings.AUTH_ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """Decode and validate a JWT access token. Returns None if invalid."""
    try:
        payload = jwt.decode(
            token, settings.AUTH_SECRET, algorithms=[settings.AUTH_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
