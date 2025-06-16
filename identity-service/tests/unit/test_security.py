# tests/unit/test_security.py
class TestSecurityMeasures:
    
    async def test_rate_limiting_login_attempts(self, test_client):
        # Test account lockout after failed attempts
        for i in range(6):
            response = await test_client.post(
                "/auth/login",
                json={"email": "test@example.com", "password": "wrong"}
            )
        
        assert response.status_code == 429
        assert "retry_after" in response.json()
    
    async def test_password_validation(self):
        # Test password strength requirements
        weak_passwords = [
            "short",
            "no-uppercase123!",
            "NO-LOWERCASE123!",
            "NoNumbers!",
            "NoSpecialChars123"
        ]
        
        for password in weak_passwords:
            assert not validate_password_strength(password)
    
    async def test_sql_injection_prevention(self, test_client):
        # Test SQL injection attempts
        malicious_email = "test@example.com'; DROP TABLE users;--"
        response = await test_client.post(
            "/auth/login",
            json={"email": malicious_email, "password": "test"}
        )
        
        assert response.status_code == 401  # Normal failed login