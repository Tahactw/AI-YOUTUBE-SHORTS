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
            'socket_timeout': 60,
            'http_chunk_size': 10485760,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'extractor_retries': 3,
            'file_access_retries': 3,
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
        
        downloaded_file = None
        
        def progress_hook(d):
            nonlocal downloaded_file
            if d['status'] == 'finished':
                downloaded_file = d['info_dict']['_filename']
        
        ydl_opts = {
            'format': 'best[height<=720]',
            'outtmpl': os.path.join(self.download_path, filename),
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [progress_hook],
            'socket_timeout': 60,
            'http_chunk_size': 10485760,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'extractor_retries': 3,
            'file_access_retries': 3,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                if downloaded_file:
                    return downloaded_file
                else:
                    raise Exception("Download completed but file name could not be determined.")
            except Exception as e:
                raise Exception(f"Error downloading video: {str(e)}")

youtube_service = YouTubeService()