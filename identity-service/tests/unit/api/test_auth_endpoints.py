# tests/unit/api/test_auth_endpoints.py
class TestAuthEndpoints(BaseAuthTest):
    
    async def test_signup_success(self, test_client, mock_auth0, sample_users):
        # Arrange
        mock_auth0.create_user.return_value = {
            "user_id": "auth0|123",
            "email": sample_users["trader"]["email"]
        }
        
        # Act
        response = await test_client.post(
            "/auth/signup",
            json=sample_users["trader"]
        )
        
        # Assert
        assert response.status_code == 201
        assert "access_token" in response.json()["auth"]
        mock_auth0.create_user.assert_called_once()
    
    async def test_signup_duplicate_email(self, test_client, mock_auth0):
        # Arrange
        mock_auth0.create_user.side_effect = Auth0Exception(
            "User already exists"
        )
        
        # Act
        response = await test_client.post(
            "/auth/signup",
            json={"email": "existing@example.com", "password": "Test123!"}
        )
        
        # Assert
        assert response.status_code == 409
        assert response.json()["code"] == "SIGNUP001"
    
    async def test_login_invalid_credentials(self, test_client, mock_auth0):
        # Test various authentication failure scenarios
        pass

# tests/unit/services/test_token_service.py
class TestTokenService:
    
    def test_decode_jwt_valid_token(self, create_test_jwt):
        # Test JWT decoding with valid token
        token = create_test_jwt({"sub": "test"})
        claims = decode_jwt(token)
        assert claims["sub"] == "test"
    
    def test_decode_jwt_expired_token(self, create_test_jwt):
        # Test expired token handling
        token = create_test_jwt({"sub": "test"}, expired=True)
        with pytest.raises(TokenExpiredException):
            decode_jwt(token)
    
    def test_extract_user_claims(self):
        # Test claim extraction logic
        pass