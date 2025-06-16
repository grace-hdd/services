# tests/conftest.py
import pytest
from datetime import datetime, timedelta
from jose import jwt
from unittest.mock import Mock, AsyncMock

@pytest.fixture
async def test_client():
    """FastAPI test client with mocked dependencies"""
    from app.main import app
    from app.dependencies import get_auth0_client, get_redis
    
    # Override dependencies
    app.dependency_overrides[get_auth0_client] = lambda: mock_auth0
    app.dependency_overrides[get_redis] = lambda: mock_redis
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
def mock_auth0_responses():
    """Common Auth0 API responses"""
    return {
        "successful_login": {
            "access_token": "test_access_token",
            "refresh_token": "test_refresh_token",
            "expires_in": 900,
            "token_type": "Bearer"
        },
        "user_profile": {
            "user_id": "auth0|123",
            "email": "test@example.com",
            "email_verified": True,
            "user_metadata": {
                "plan": "starter"
            },
            "app_metadata": {
                "roles": ["user"],
                "quotas": {
                    "backtests_per_month": 100
                }
            }
        }
    }

@pytest.fixture
def create_test_jwt():
    """Factory for creating test JWT tokens"""
    def _create_jwt(claims, expired=False):
        now = datetime.utcnow()
        exp = now - timedelta(hours=1) if expired else now + timedelta(hours=1)
        
        token_data = {
            "iss": "https://test.auth0.com/",
            "aud": "test-audience",
            "iat": now,
            "exp": exp,
            **claims
        }
        
        return jwt.encode(
            token_data,
            "test-secret",
            algorithm="HS256"
        )
    return _create_jwt

@pytest.fixture
def sample_users():
    """Test user data"""
    return {
        "trader": {
            "email": "trader@example.com",
            "password": "SecurePass123!",
            "name": "Test Trader",
            "user_type": "trader"
        },
        "investor": {
            "email": "investor@example.com",
            "password": "SecurePass456!",
            "name": "Test Investor",
            "user_type": "investor"
        }
    }