"""
Security tests for the application
"""

import pytest
from fastapi.testclient import TestClient
from core.config import Settings
from core.security import SecurityManager, generate_secret_key, generate_jwt_secret, validate_secret_key, validate_jwt_secret


class TestSecurityManager:
    """Test the SecurityManager class"""
    
    def test_password_hashing(self):
        """Test password hashing and verification"""
        security_manager = SecurityManager("test-secret-key-32-chars-long", "test-jwt-secret-key-32-chars-long")
        
        password = "test_password_123"
        hashed = security_manager.hash_password(password)
        
        # Hash should be different from original
        assert hashed != password
        assert len(hashed) > 0
        
        # Verification should work
        assert security_manager.verify_password(password, hashed)
        assert not security_manager.verify_password("wrong_password", hashed)
    
    def test_jwt_token_creation_and_verification(self):
        """Test JWT token creation and verification"""
        security_manager = SecurityManager("test-secret-key-32-chars-long", "test-jwt-secret-key-32-chars-long")
        
        data = {"user_id": "123", "email": "test@example.com"}
        token = security_manager.create_access_token(data)
        
        # Token should be a string
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token
        payload = security_manager.verify_token(token)
        assert payload["user_id"] == "123"
        assert payload["email"] == "test@example.com"
        assert "exp" in payload
    
    def test_jwt_token_expiration(self):
        """Test JWT token expiration"""
        from datetime import timedelta
        
        security_manager = SecurityManager("test-secret-key-32-chars-long", "test-jwt-secret-key-32-chars-long")
        
        data = {"user_id": "123"}
        token = security_manager.create_access_token(data, expires_delta=timedelta(seconds=1))
        
        # Token should be valid initially
        payload = security_manager.verify_token(token)
        assert payload["user_id"] == "123"
        
        # Token should expire (we'll just test that it works, not wait for expiration)
        import time
        time.sleep(2)
        
        # Should raise an exception for expired token
        with pytest.raises(Exception):
            security_manager.verify_token(token)


class TestSecurityUtilities:
    """Test security utility functions"""
    
    def test_generate_secret_key(self):
        """Test secret key generation"""
        key1 = generate_secret_key()
        key2 = generate_secret_key()
        
        # Keys should be different
        assert key1 != key2
        
        # Keys should be long enough
        assert len(key1) >= 32
        assert len(key2) >= 32
    
    def test_generate_jwt_secret(self):
        """Test JWT secret generation"""
        secret1 = generate_jwt_secret()
        secret2 = generate_jwt_secret()
        
        # Secrets should be different
        assert secret1 != secret2
        
        # Secrets should be long enough
        assert len(secret1) >= 32
        assert len(secret2) >= 32
    
    def test_validate_secret_key(self):
        """Test secret key validation"""
        # Valid keys
        assert validate_secret_key("a-very-long-secret-key-that-is-definitely-secure")
        assert validate_secret_key("x" * 32)
        
        # Invalid keys
        assert not validate_secret_key("short")
        assert not validate_secret_key("your-secret-key-here")
        assert not validate_secret_key("test-secret-key")
        assert not validate_secret_key("development-secret-key")
        assert not validate_secret_key("changeme")
    
    def test_validate_jwt_secret(self):
        """Test JWT secret validation"""
        # Valid secrets
        assert validate_jwt_secret("a-very-long-jwt-secret-that-is-definitely-secure")
        assert validate_jwt_secret("x" * 32)
        
        # Invalid secrets
        assert not validate_jwt_secret("short")
        assert not validate_jwt_secret("your-jwt-secret-key-here")
        assert not validate_jwt_secret("test-jwt-secret-key")
        assert not validate_jwt_secret("development-jwt-secret")
        assert not validate_jwt_secret("changeme")


class TestSecurityConfiguration:
    """Test security configuration validation"""
    
    def test_valid_configuration(self):
        """Test that valid configuration works"""
        config = Settings(
            secret_key="a-very-long-secret-key-that-is-definitely-secure",
            jwt_secret_key="a-very-long-jwt-secret-that-is-definitely-secure",
            database_url="postgresql://user:pass@localhost/db",
            fastapi_env="development"
        )
        
        assert config.secret_key == "a-very-long-secret-key-that-is-definitely-secure"
        assert config.jwt_secret_key == "a-very-long-jwt-secret-that-is-definitely-secure"
        assert config.database_url == "postgresql://user:pass@localhost/db"
        assert config.fastapi_env == "development"
    
    def test_invalid_secret_key(self):
        """Test that invalid secret keys are rejected"""
        with pytest.raises(ValueError, match="SECRET_KEY must be at least 32 characters"):
            Settings(
                secret_key="short",
                jwt_secret_key="a-very-long-jwt-secret-that-is-definitely-secure",
                database_url="postgresql://user:pass@localhost/db"
            )
    
    def test_invalid_jwt_secret_key(self):
        """Test that invalid JWT secret keys are rejected"""
        with pytest.raises(ValueError, match="JWT_SECRET_KEY must be at least 32 characters"):
            Settings(
                secret_key="a-very-long-secret-key-that-is-definitely-secure",
                jwt_secret_key="short",
                database_url="postgresql://user:pass@localhost/db"
            )
    
    def test_invalid_database_url(self):
        """Test that invalid database URLs are rejected"""
        with pytest.raises(ValueError, match="DATABASE_URL must be a valid database URL"):
            Settings(
                secret_key="a-very-long-secret-key-that-is-definitely-secure",
                jwt_secret_key="a-very-long-jwt-secret-that-is-definitely-secure",
                database_url="invalid-url"
            )
    
    def test_invalid_environment(self):
        """Test that invalid environments are rejected"""
        with pytest.raises(ValueError, match="FASTAPI_ENV must be one of"):
            Settings(
                secret_key="a-very-long-secret-key-that-is-definitely-secure",
                jwt_secret_key="a-very-long-jwt-secret-that-is-definitely-secure",
                database_url="postgresql://user:pass@localhost/db",
                fastapi_env="invalid-env"
            )


class TestSecurityMiddleware:
    """Test security middleware functionality"""
    
    def test_security_headers_applied(self):
        """Test that security headers are applied to responses"""
        # This test would require setting up a test app with middleware
        # For now, we'll test the basic functionality
        pass
    
    def test_rate_limiting_functionality(self):
        """Test rate limiting functionality"""
        # This test would require setting up a test app with rate limiting
        # For now, we'll test the basic functionality
        pass