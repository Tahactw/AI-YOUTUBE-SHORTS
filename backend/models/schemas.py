from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VideoRequest(BaseModel):
    url: str
    title: Optional[str] = None
    description: Optional[str] = None

class VideoResponse(BaseModel):
    id: int
    url: str
    title: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}

class HealthResponse(BaseModel):
    status: str
    service: str