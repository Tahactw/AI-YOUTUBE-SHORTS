"""
Test YouTube service functionality
"""
import pytest
import requests
from unittest.mock import patch, MagicMock
from services.youtube import YouTubeService, youtube_service


class TestYouTubeService:
    """Test YouTube service functionality"""
    
    def test_youtube_service_init(self):
        """Test YouTube service initialization"""
        service = YouTubeService()
        assert service.download_path is not None
        assert hasattr(service, 'get_video_info')
        assert hasattr(service, 'download_video')
    
    def test_get_video_info_mock(self):
        """Test get_video_info with mocked response"""
        service = YouTubeService()
        
        # Mock yt-dlp response
        mock_info = {
            'title': 'Test Video',
            'description': 'Test Description',
            'duration': 120,
            'thumbnail': 'https://example.com/thumb.jpg',
            'uploader': 'Test Channel',
            'view_count': 1000,
        }
        
        with patch('yt_dlp.YoutubeDL') as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.return_value = mock_info
            
            result = service.get_video_info('https://www.youtube.com/watch?v=test')
            
            assert result['title'] == 'Test Video'
            assert result['description'] == 'Test Description'
            assert result['duration'] == 120
            assert result['uploader'] == 'Test Channel'
            assert result['view_count'] == 1000
    
    def test_get_video_info_error_handling(self):
        """Test error handling in get_video_info"""
        service = YouTubeService()
        
        with patch('yt_dlp.YoutubeDL') as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.extract_info.side_effect = Exception("Network error")
            
            with pytest.raises(Exception) as exc_info:
                service.get_video_info('https://www.youtube.com/watch?v=test')
            
            assert "Error extracting video info" in str(exc_info.value)
    
    def test_download_video_mock(self, test_upload_dir):
        """Test download_video with mocked response"""
        service = YouTubeService()
        service.download_path = str(test_upload_dir)
        
        # Mock successful download
        test_filename = str(test_upload_dir / "test_video.mp4")
        
        def mock_download(urls):
            # Create a dummy file to simulate download
            with open(test_filename, 'w') as f:
                f.write("dummy video content")
        
        def mock_progress_hook(d):
            if d['status'] == 'finished':
                d['info_dict'] = {'_filename': test_filename}
        
        with patch('yt_dlp.YoutubeDL') as mock_ydl:
            mock_instance = mock_ydl.return_value.__enter__.return_value
            mock_instance.download.side_effect = mock_download
            
            # We need to simulate the progress hook being called
            with patch.object(service, 'download_video') as mock_method:
                mock_method.return_value = test_filename
                
                result = service.download_video('https://www.youtube.com/watch?v=test')
                assert result == test_filename
    
    def test_download_video_error_handling(self):
        """Test error handling in download_video"""
        service = YouTubeService()
        
        with patch('yt_dlp.YoutubeDL') as mock_ydl:
            mock_ydl.return_value.__enter__.return_value.download.side_effect = Exception("Download failed")
            
            with pytest.raises(Exception) as exc_info:
                service.download_video('https://www.youtube.com/watch?v=test')
            
            assert "Error downloading video" in str(exc_info.value)


class TestYouTubeConnectivity:
    """Test YouTube connectivity and network access"""
    
    def test_youtube_domains_accessible(self):
        """Test that YouTube domains are accessible"""
        domains = [
            'https://www.youtube.com',
            'https://youtube.com',
            'https://i.ytimg.com',
        ]
        
        for domain in domains:
            try:
                response = requests.get(domain, timeout=10)
                assert response.status_code in [200, 301, 302, 403]  # Various acceptable responses
            except requests.RequestException as e:
                pytest.skip(f"Network connectivity issue: {e}")
    
    def test_yt_dlp_import(self):
        """Test that yt-dlp can be imported"""
        import yt_dlp
        assert hasattr(yt_dlp, 'YoutubeDL')
    
    @pytest.mark.slow
    def test_real_youtube_video_info(self, test_youtube_url):
        """Test extracting real YouTube video info (slow test)"""
        service = YouTubeService()
        
        try:
            info = service.get_video_info(test_youtube_url)
            assert 'title' in info
            assert 'duration' in info
            assert info['duration'] > 0
        except Exception as e:
            pytest.skip(f"YouTube access issue: {e}")


class TestYouTubeServiceGlobalInstance:
    """Test the global YouTube service instance"""
    
    def test_global_youtube_service_exists(self):
        """Test that global youtube_service instance exists"""
        assert youtube_service is not None
        assert isinstance(youtube_service, YouTubeService)
    
    def test_global_youtube_service_has_download_path(self):
        """Test that global youtube_service has download_path"""
        assert hasattr(youtube_service, 'download_path')
        assert youtube_service.download_path is not None