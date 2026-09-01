"""
Integration tests for Authentication API endpoints.
"""

import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    """Test user registration."""
    response = await async_client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "strongpassword123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "id" in data

@pytest.mark.asyncio
async def test_register_duplicate_user(async_client: AsyncClient):
    """Test registering a user that already exists."""
    # Register first
    await async_client.post(
        "/api/auth/register",
        json={
            "email": "dup@example.com",
            "password": "strongpassword123",
            "full_name": "Dup User"
        }
    )
    
    # Try again
    response = await async_client.post(
        "/api/auth/register",
        json={
            "email": "dup@example.com",
            "password": "anotherpassword",
            "full_name": "Dup User Two"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient):
    """Test user login and token generation."""
    # Register first
    await async_client.post(
        "/api/auth/register",
        json={
            "email": "login@example.com",
            "password": "loginpassword",
            "full_name": "Login User"
        }
    )
    
    # Login
    response = await async_client.post(
        "/api/auth/login",
        data={
            "username": "login@example.com",
            "password": "loginpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_get_current_user(async_client: AsyncClient):
    """Test retrieving current authenticated user details."""
    # Register and Login
    await async_client.post(
        "/api/auth/register",
        json={
            "email": "me@example.com",
            "password": "mepassword",
            "full_name": "Me User"
        }
    )
    login_resp = await async_client.post(
        "/api/auth/login",
        data={
            "username": "me@example.com",
            "password": "mepassword"
        }
    )
    token = login_resp.json()["access_token"]
    
    # Get Me
    me_resp = await async_client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_resp.status_code == 200
    data = me_resp.json()
    assert data["email"] == "me@example.com"
    assert data["full_name"] == "Me User"
