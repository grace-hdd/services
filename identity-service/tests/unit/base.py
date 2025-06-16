# tests/unit/base.py
import pytest
from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient

class BaseAuthTest:
    """Base class for authentication tests"""
    
    @pytest.fixture
    def mock_auth0(self):
        """Mock Auth0 Management and Authentication APIs"""
        mock = Mock()
        mock.create_user = AsyncMock()
        mock.authenticate = AsyncMock()
        mock.update_user = AsyncMock()
        mock.get_user = AsyncMock()
        return mock
    
    @pytest.fixture
    def valid_jwt_token(self):
        """Generate valid test JWT token"""
        return create_test_jwt({
            "sub": "auth0|test123",
            "email": "test@example.com",
            "https://coinquant.io/claims": {
                "user_id": "test-uuid",
                "plan": "starter",
                "roles": ["user"]
            }
        })

class BaseSessionTest:
    """Base class for session management tests"""
    
    @pytest.fixture
    async def mock_redis(self):
        """Mock Redis for session storage"""
        return create_mock_redis()