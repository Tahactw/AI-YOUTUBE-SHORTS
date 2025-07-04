from pydantic import BaseModel, HttpUrl, validator
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum
import re


class DownloadStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class YouTubeUrlRequest(BaseModel):
    url: str
    
    @validator('url')
    def validate_youtube_url(cls, v):
        """Validate that the URL is a valid YouTube URL"""
        youtube_regex = re.compile(
            r'^https?://(www\.)?(youtube\.com/(watch\?v=|embed/|v/)|youtu\.be/|m\.youtube\.com/watch\?v=)[a-zA-Z0-9_-]{11}$'
        )
        if not youtube_regex.match(v):
            raise ValueError('Invalid YouTube URL format')
        return v


class VideoMetadata(BaseModel):
    title: str
    description: Optional[str] = None
    duration: int  # in seconds
    thumbnail: Optional[str] = None
    uploader: Optional[str] = None
    view_count: Optional[int] = None
    upload_date: Optional[str] = None


class DownloadRequest(BaseModel):
    job_id: str
    url: str
    status: DownloadStatus
    created_at: datetime
    metadata: Optional[VideoMetadata] = None


class DownloadResponse(BaseModel):
    job_id: str
    status: DownloadStatus
    message: str
    created_at: datetime
    metadata: Optional[VideoMetadata] = None
    file_path: Optional[str] = None
    error_details: Optional[str] = None


class DownloadStatusResponse(BaseModel):
    job_id: str
    status: DownloadStatus
    progress: Optional[float] = None  # 0-100 percentage
    message: str
    file_path: Optional[str] = None
    error_details: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None


class MetadataResponse(BaseModel):
    success: bool
    metadata: Optional[VideoMetadata] = None
    error: Optional[str] = None