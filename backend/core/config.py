import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict, Field, field_validator
from functools import lru_cache


class Settings(BaseSettings):
    # Environment settings
    fastapi_env: str = Field(default="development", description="Environment: development, test, production")
    
    # FastAPI settings
    app_name: str = Field(default="AI YouTube Shorts SaaS", description="Application name")
    debug: bool = Field(default=True, description="Debug mode")
    secret_key: str = Field(..., description="Secret key for sessions and encryption")
    jwt_secret_key: str = Field(..., description="JWT secret key for token signing")
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_expire_minutes: int = Field(default=30, description="JWT token expiration in minutes")
    
    # Database settings
    database_url: str = Field(..., description="Database connection URL")
    database_ssl_require: bool = Field(default=False, description="Require SSL for database connections")
    
    # Redis settings
    redis_url: str = Field(default="redis://localhost:6379", description="Redis connection URL")
    redis_ssl: bool = Field(default=False, description="Use SSL for Redis connections")
    
    # OpenAI settings
    openai_api_key: str = Field(default="", description="OpenAI API key")
    
    # YouTube API settings
    youtube_api_key: str = Field(default="", description="YouTube API key")
    
    # File upload settings
    upload_dir: str = Field(default="uploads", description="Directory for file uploads")
    max_upload_size: int = Field(default=100 * 1024 * 1024, description="Maximum upload size in bytes")
    
    # Celery settings
    celery_broker_url: str = Field(default="redis://localhost:6379", description="Celery broker URL")
    celery_result_backend: str = Field(default="redis://localhost:6379", description="Celery result backend URL")
    
    # Security settings
    allowed_origins: List[str] = Field(default=["http://localhost:3000"], description="Allowed CORS origins")
    allowed_methods: List[str] = Field(default=["GET", "POST", "PUT", "DELETE"], description="Allowed HTTP methods")
    rate_limit_requests: int = Field(default=100, description="Rate limit requests per minute")
    rate_limit_period: int = Field(default=60, description="Rate limit period in seconds")
    
    @field_validator('secret_key')
    @classmethod
    def validate_secret_key(cls, v):
        """Validate secret key meets security requirements"""
        if not v:
            raise ValueError('SECRET_KEY is required')
        if len(v) < 32:
            raise ValueError('SECRET_KEY must be at least 32 characters long')
        if v in ['your-secret-key-here', 'test-secret-key', 'development-secret-key', 'changeme']:
            raise ValueError('SECRET_KEY must not use default/weak values')
        return v
    
    @field_validator('jwt_secret_key')
    @classmethod
    def validate_jwt_secret_key(cls, v):
        """Validate JWT secret key meets security requirements"""
        if not v:
            raise ValueError('JWT_SECRET_KEY is required')
        if len(v) < 32:
            raise ValueError('JWT_SECRET_KEY must be at least 32 characters long')
        if v in ['your-jwt-secret-key-here', 'test-jwt-secret-key', 'development-jwt-secret', 'changeme']:
            raise ValueError('JWT_SECRET_KEY must not use default/weak values')
        return v
    
    @field_validator('database_url')
    @classmethod
    def validate_database_url(cls, v):
        """Validate database URL format"""
        if not v:
            raise ValueError('DATABASE_URL is required')
        if not v.startswith(('postgresql://', 'mysql://', 'sqlite://')):
            raise ValueError('DATABASE_URL must be a valid database URL')
        return v
    
    @field_validator('allowed_origins')
    @classmethod
    def validate_allowed_origins(cls, v):
        """Validate allowed origins"""
        if not v:
            raise ValueError('At least one allowed origin must be specified')
        return v
    
    @field_validator('fastapi_env')
    @classmethod
    def validate_environment(cls, v):
        """Validate environment setting"""
        if v not in ['development', 'test', 'production']:
            raise ValueError('FASTAPI_ENV must be one of: development, test, production')
        return v
    
    model_config = ConfigDict(
        env_file=[".env.test", ".env"],  # Try test env first, then regular env
        case_sensitive=False,
        extra='ignore',  # This allows extra environment variables
        validate_default=True
    )


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# For backward compatibility - only create if needed
def get_settings_safe() -> Optional[Settings]:
    """Get settings safely without raising validation errors"""
    try:
        return get_settings()
    except Exception:
        return None
