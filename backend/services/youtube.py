import yt_dlp
import os
import time
import logging
from typing import Dict, Any, List, Optional
from core.config import settings

# Configure logging
logger = logging.getLogger(__name__)

class YouTubeService:
    # Default fallback video IDs for testing
    DEFAULT_FALLBACK_VIDEO_IDS = [
        "dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up (very stable)
        "9bZkp7q19f0",  # Alternative stable video
        "jNQXAC9IVRw",  # Public domain/creative commons video
        "BaW_jenozKc",  # Original failing video (keep as fallback)
    ]
    
    def __init__(self):
        self.download_path = settings.upload_dir
        os.makedirs(self.download_path, exist_ok=True)
    
    def _get_ydl_options(self, for_download: bool = False) -> Dict[str, Any]:
        """Get standardized yt-dlp options with robust error handling"""
        base_opts = {
            'quiet': True,
            'no_warnings': True,
            'socket_timeout': 60,
            'http_chunk_size': 10485760,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'referer': 'https://www.youtube.com/',
            'extractor_retries': 3,
            'file_access_retries': 3,
            'fragment_retries': 3,
            'retry_sleep_functions': {
                'http': lambda n: min(4 ** n, 60),
                'fragment': lambda n: min(4 ** n, 60),
                'extractor': lambda n: min(4 ** n, 60),
            },
        }
        
        if for_download:
            base_opts.update({
                'format': 'best[height<=720]',
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            })
        
        return base_opts
    
    def get_video_info_with_fallback(self, video_ids: List[str]) -> Dict[str, Any]:
        """
        Get video information with fallback mechanism
        Tries multiple video IDs until one succeeds
        """
        last_error = None
        
        for i, video_id in enumerate(video_ids):
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            try:
                logger.info(f"Attempting to get video info for: {video_id} (attempt {i+1}/{len(video_ids)})")
                return self.get_video_info(url)
            except Exception as e:
                last_error = e
                logger.warning(f"Failed to get video info for {video_id}: {str(e)}")
                
                # Add a small delay between attempts
                if i < len(video_ids) - 1:
                    time.sleep(2)
                    
        # If all fallbacks failed, raise the last error
        if last_error:
            raise Exception(f"All fallback video IDs failed. Last error: {str(last_error)}")
        else:
            raise Exception("No video IDs provided for fallback")
    
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """Get video information without downloading"""
        ydl_opts = self._get_ydl_options(for_download=False)
        
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
                    'url': url,
                }
            except Exception as e:
                error_msg = f"Error extracting video info from {url}: {str(e)}"
                logger.error(error_msg)
                raise Exception(error_msg)
    
    def download_video_with_fallback(self, video_ids: List[str], filename: str = None) -> str:
        """
        Download video with fallback mechanism
        Tries multiple video IDs until one succeeds
        """
        last_error = None
        
        for i, video_id in enumerate(video_ids):
            url = f"https://www.youtube.com/watch?v={video_id}"
            
            try:
                logger.info(f"Attempting to download video: {video_id} (attempt {i+1}/{len(video_ids)})")
                return self.download_video(url, filename)
            except Exception as e:
                last_error = e
                logger.warning(f"Failed to download video {video_id}: {str(e)}")
                
                # Add a small delay between attempts
                if i < len(video_ids) - 1:
                    time.sleep(2)
                    
        # If all fallbacks failed, raise the last error
        if last_error:
            raise Exception(f"All fallback video IDs failed. Last error: {str(last_error)}")
        else:
            raise Exception("No video IDs provided for fallback")
    
    def download_video(self, url: str, filename: str = None) -> str:
        """Download video from YouTube"""
        if filename is None:
            filename = '%(title)s.%(ext)s'
        
        downloaded_file = None
        
        def progress_hook(d):
            nonlocal downloaded_file
            if d['status'] == 'finished':
                downloaded_file = d['info_dict']['_filename']
        
        ydl_opts = self._get_ydl_options(for_download=True)
        ydl_opts['progress_hooks'] = [progress_hook]
        
        if filename != '%(title)s.%(ext)s':
            ydl_opts['outtmpl'] = os.path.join(self.download_path, filename)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                if downloaded_file:
                    return downloaded_file
                else:
                    raise Exception("Download completed but file name could not be determined.")
            except Exception as e:
                error_msg = f"Error downloading video from {url}: {str(e)}"
                logger.error(error_msg)
                raise Exception(error_msg)

youtube_service = YouTubeService()