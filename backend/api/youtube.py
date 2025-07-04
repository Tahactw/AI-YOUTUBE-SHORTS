from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, Any
from datetime import datetime
import logging

from models.youtube_models import (
    YouTubeUrlRequest, 
    DownloadResponse, 
    DownloadStatusResponse, 
    ErrorResponse,
    MetadataResponse,
    VideoMetadata,
    DownloadStatus
)
from services.youtube import youtube_service
from core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/download", response_model=DownloadResponse)
async def download_youtube_video(
    request: YouTubeUrlRequest,
    background_tasks: BackgroundTasks
):
    """
    Download a YouTube video
    
    - **url**: Valid YouTube URL
    - Returns job ID for tracking download progress
    """
    try:
        # Validate URL
        if not youtube_service.validate_youtube_url(request.url):
            raise HTTPException(
                status_code=400,
                detail="Invalid YouTube URL format"
            )
        
        # Generate job ID
        job_id = youtube_service.generate_job_id()
        
        # Get video metadata first
        try:
            metadata_dict = youtube_service.get_video_info(request.url)
            metadata = VideoMetadata(**metadata_dict)
        except Exception as e:
            logger.error(f"Error getting video metadata: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"Error getting video metadata: {str(e)}"
            )
        
        # Initialize job
        youtube_service.update_job_status(
            job_id, 
            DownloadStatus.PENDING, 
            url=request.url, 
            metadata=metadata_dict,
            created_at=datetime.now()
        )
        
        # Start download in background
        background_tasks.add_task(
            youtube_service.download_video,
            request.url,
            job_id
        )
        
        return DownloadResponse(
            job_id=job_id,
            status=DownloadStatus.PENDING,
            message="Download started successfully",
            created_at=datetime.now(),
            metadata=metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in download endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/download/{job_id}/status", response_model=DownloadStatusResponse)
async def get_download_status(job_id: str):
    """
    Get download status by job ID
    
    - **job_id**: Job ID returned from download endpoint
    """
    try:
        job_info = youtube_service.get_job_status(job_id)
        
        if not job_info:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )
        
        return DownloadStatusResponse(
            job_id=job_id,
            status=job_info.get('status', DownloadStatus.PENDING),
            progress=job_info.get('progress'),
            message=job_info.get('message', 'Download in progress'),
            file_path=job_info.get('file_path'),
            error_details=job_info.get('error_details')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting download status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/metadata", response_model=MetadataResponse)
async def get_video_metadata(request: YouTubeUrlRequest):
    """
    Get video metadata without downloading
    
    - **url**: Valid YouTube URL
    """
    try:
        # Validate URL
        if not youtube_service.validate_youtube_url(request.url):
            raise HTTPException(
                status_code=400,
                detail="Invalid YouTube URL format"
            )
        
        # Get metadata
        metadata_dict = youtube_service.get_video_info(request.url)
        metadata = VideoMetadata(**metadata_dict)
        
        return MetadataResponse(
            success=True,
            metadata=metadata
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting video metadata: {str(e)}")
        return MetadataResponse(
            success=False,
            error=str(e)
        )


@router.get("/jobs", response_model=Dict[str, Any])
async def list_jobs():
    """
    List all download jobs (for debugging/monitoring)
    """
    try:
        jobs = youtube_service.jobs
        return {
            "total_jobs": len(jobs),
            "jobs": jobs
        }
    except Exception as e:
        logger.error(f"Error listing jobs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.post("/test-mode")
async def toggle_test_mode(enable: bool = True):
    """
    Toggle test mode for development/testing
    
    - **enable**: True to enable test mode, False to disable
    """
    try:
        # In production, this would be protected by authentication
        settings.youtube_test_mode = enable
        return {
            "message": f"Test mode {'enabled' if enable else 'disabled'}",
            "test_mode": settings.youtube_test_mode
        }
    except Exception as e:
        logger.error(f"Error toggling test mode: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@router.get("/test-mode")
async def get_test_mode():
    """
    Get current test mode status
    """
    return {
        "test_mode": settings.youtube_test_mode
    }


@router.delete("/jobs/{job_id}")
async def cancel_job(job_id: str):
    """
    Cancel a download job
    
    - **job_id**: Job ID to cancel
    """
    try:
        if job_id not in youtube_service.jobs:
            raise HTTPException(
                status_code=404,
                detail="Job not found"
            )
        
        # Update job status to cancelled
        youtube_service.update_job_status(
            job_id, 
            DownloadStatus.FAILED, 
            error_details="Job cancelled by user"
        )
        
        return {"message": "Job cancelled successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling job: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )