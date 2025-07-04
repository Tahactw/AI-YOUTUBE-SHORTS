import yt_dlp
import os
from typing import Dict, Any
from core.config import settings

class YouTubeService:
    def __init__(self):
        self.download_path = settings.upload_dir
        os.makedirs(self.download_path, exist_ok=True)
    
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """Get video information without downloading"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', ''),
                    'description': info.get('description', ''),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', ''),
                    'view_count': info.get('view_count', 0),
                }
            except Exception as e:
                raise Exception(f"Error extracting video info: {str(e)}")
    
    def download_video(self, url: str, filename: str = None) -> str:
        """Download video from YouTube"""
        if filename is None:
            filename = '%(title)s.%(ext)s'
        
        ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': os.path.join(self.download_path, filename),
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                return os.path.join(self.download_path, filename)
            except Exception as e:
                raise Exception(f"Error downloading video: {str(e)}")

youtube_service = YouTubeService()