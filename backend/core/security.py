"""
Security utilities for authentication and encryption
"""

import secrets
from typing import Optional, Dict, Any
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token handling
security = HTTPBearer()


class SecurityManager:
    """Security manager for authentication and token handling"""
    
    def __init__(self, secret_key: str, jwt_secret_key: str, algorithm: str = "HS256", expire_minutes: int = 30):
        self.pwd_context = pwd_context
        self.algorithm = algorithm
        self.secret_key = secret_key
        self.jwt_secret_key = jwt_secret_key
        self.expire_minutes = expire_minutes
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.jwt_secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )


def generate_secret_key() -> str:
    """Generate a cryptographically secure secret key"""
    return secrets.token_urlsafe(32)


def generate_jwt_secret() -> str:
    """Generate a cryptographically secure JWT secret"""
    return secrets.token_urlsafe(32)


def validate_secret_key(secret_key: str) -> bool:
    """Validate that a secret key meets security requirements"""
    return len(secret_key) >= 32 and secret_key not in [
        "your-secret-key-here",
        "test-secret-key",
        "development-secret-key",
        "changeme"
    ]


def validate_jwt_secret(jwt_secret: str) -> bool:
    """Validate that a JWT secret meets security requirements"""
    return len(jwt_secret) >= 32 and jwt_secret not in [
        "your-jwt-secret-key-here",
        "test-jwt-secret-key",
        "development-jwt-secret",
        "changeme"
    ]