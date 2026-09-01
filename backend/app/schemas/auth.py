"""
Authentication schemas.

Pydantic models for user registration, login, and token responses.
"""

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password (min 8 chars)")
    full_name: str | None = Field(None, description="User's full name")


class UserLogin(BaseModel):
    """Schema for user login (alternative to OAuth2 password flow)."""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")


class UserResponse(BaseModel):
    """Schema for returning user data."""
    id: str
    email: EmailStr
    full_name: str | None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT access token."""
    access_token: str
    token_type: str = "bearer"
