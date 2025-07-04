import os
from pydantic_settings import BaseSettings

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
    
    # YouTube download settings
    youtube_download_dir: str = "downloads"
    youtube_max_file_size: int = 500 * 1024 * 1024  # 500MB
    youtube_allowed_formats: list = ["mp4", "webm", "mkv"]  # Allowed formats for YouTube downloads. Enforce in the download service.
    youtube_max_duration: int = 3600  # 1 hour in seconds
    youtube_download_timeout: int = 300  # 5 minutes. Enforce as a timeout in the download service.
    youtube_test_mode: bool = False  # Enable test mode for development
    
    # Celery settings
    celery_broker_url: str = "redis://localhost:6379"
    celery_result_backend: str = "redis://localhost:6379"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()