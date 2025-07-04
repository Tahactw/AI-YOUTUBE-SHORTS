import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # FastAPI settings
    app_name: str = "AI YouTube Shorts SaaS"
    debug: bool = True
    secret_key: str = "your-secret-key-here"
    jwt_secret_key: str = "your-jwt-secret-key-here"
    
    # Database settings
    database_url: str = "postgresql://postgres:postgres@localhost:5432/ai_youtube_shorts"
    
    # Redis settings
    redis_url: str = "redis://localhost:6379"
    
    # OpenAI settings
    openai_api_key: str = ""
    
    # YouTube API settings
    youtube_api_key: str = ""
    
    # File upload settings
    upload_dir: str = "uploads"
    max_upload_size: int = 100 * 1024 * 1024  # 100MB
    
    # Celery settings
    celery_broker_url: str = "redis://localhost:6379"
    celery_result_backend: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()