import yt_dlp
import os
import uuid
import logging
from typing import Dict, Any, Optional
from core.config import settings
from models.youtube_models import VideoMetadata, DownloadStatus
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self):
        self.download_path = settings.youtube_download_dir
        self.upload_path = settings.upload_dir
        os.makedirs(self.download_path, exist_ok=True)
        os.makedirs(self.upload_path, exist_ok=True)
        
        # In-memory storage for job tracking (in production, use Redis/Database)
        self.jobs = {}
    
    def validate_youtube_url(self, url: str) -> bool:
        """Validate YouTube URL format"""
        youtube_regex = re.compile(
            r'^https?://(www\.)?(youtube\.com/(watch\?v=|embed/|v/)|youtu\.be/|m\.youtube\.com/watch\?v=)[a-zA-Z0-9_-]{11}$'
        )
        return bool(youtube_regex.match(url))
    
    def generate_job_id(self) -> str:
        """Generate unique job ID for tracking"""
        return str(uuid.uuid4())
    
    def update_job_status(self, job_id: str, status: DownloadStatus, **kwargs):
        """Update job status and additional information"""
        if job_id in self.jobs:
            self.jobs[job_id].update({
                'status': status,
                **kwargs
            })
        else:
            self.jobs[job_id] = {
                'status': status,
                **kwargs
            }
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status and information"""
        return self.jobs.get(job_id)
    
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """Get video information without downloading"""
        if not self.validate_youtube_url(url):
            raise ValueError("Invalid YouTube URL format")
        
        # Test mode - return mock data
        if settings.youtube_test_mode:
            return {
                'title': 'Test Video Title',
                'description': 'This is a test video description',
                'duration': 180,  # 3 minutes
                'thumbnail': 'https://example.com/thumbnail.jpg',
                'uploader': 'Test Uploader',
                'view_count': 1000000,
                'upload_date': '20240101',
            }
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Check video duration
                duration = info.get('duration', 0)
                if duration > settings.youtube_max_duration:
                    raise ValueError(f"Video too long: {duration}s (max: {settings.youtube_max_duration}s)")
                
                return {
                    'title': info.get('title', ''),
                    'description': info.get('description', ''),
                    'duration': duration,
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', ''),
                    'view_count': info.get('view_count', 0),
                    'upload_date': info.get('upload_date', ''),
                }
        except Exception as e:
            logger.error(f"Error extracting video info: {str(e)}")
            raise Exception(f"Error extracting video info: {str(e)}")
    
    def download_video(self, url: str, job_id: str = None, filename: str = None) -> str:
        """Download video from YouTube"""
        if not self.validate_youtube_url(url):
            raise ValueError("Invalid YouTube URL format")
        
        if job_id is None:
            job_id = self.generate_job_id()
        
        if filename is None:
            filename = '%(title)s.%(ext)s'
        
        # Initialize job status
        self.update_job_status(job_id, DownloadStatus.PENDING, url=url)
        
        # Test mode - create a mock file
        if settings.youtube_test_mode:
            # Create a test file
            test_filename = f"test_video_{job_id}.mp4"
            test_path = os.path.join(self.download_path, test_filename)
            
            # Create a small test file
            with open(test_path, 'w') as f:
                f.write("# Test video file - this would be the actual video content")
            
            self.update_job_status(job_id, DownloadStatus.COMPLETED, file_path=test_path)
            return test_path
        
        downloaded_file = None
        
        def progress_hook(d):
            nonlocal downloaded_file
            if d['status'] == 'downloading':
                self.update_job_status(job_id, DownloadStatus.IN_PROGRESS, 
                                     progress=float(d.get('_percent_str', '0%').strip('%')))
            elif d['status'] == 'finished':
                downloaded_file = d.get('filename', d.get('_filename', ''))
                self.update_job_status(job_id, DownloadStatus.COMPLETED,
                                     file_path=downloaded_file)
        
        ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': os.path.join(self.download_path, filename),
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [progress_hook],
            'extractaudio': False,
            'audioformat': 'mp3',
            'max_filesize': settings.youtube_max_file_size,
            'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
                if downloaded_file and os.path.exists(downloaded_file):
                    return downloaded_file
                else:
                    error_msg = "Download completed but file could not be found"
                    self.update_job_status(job_id, DownloadStatus.FAILED, 
                                         error_details=error_msg)
                    raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error downloading video: {str(e)}"
            logger.error(error_msg)
            self.update_job_status(job_id, DownloadStatus.FAILED, 
                                 error_details=error_msg)
            raise Exception(error_msg)
    
    async def download_video_async(self, url: str, job_id: str = None) -> Dict[str, Any]:
        """Async wrapper for video download with job tracking"""
        if job_id is None:
            job_id = self.generate_job_id()
        
        try:
            # Get video metadata first
            metadata = self.get_video_info(url)
            
            # Update job with metadata
            self.update_job_status(job_id, DownloadStatus.PENDING, 
                                 url=url, metadata=metadata)
            
            # Download video
            file_path = self.download_video(url, job_id)
            
            return {
                'job_id': job_id,
                'status': DownloadStatus.COMPLETED,
                'file_path': file_path,
                'metadata': metadata
            }
        except Exception as e:
            error_msg = str(e)
            self.update_job_status(job_id, DownloadStatus.FAILED, 
                                 error_details=error_msg)
            return {
                'job_id': job_id,
                'status': DownloadStatus.FAILED,
                'error_details': error_msg
            }

youtube_service = YouTubeService()