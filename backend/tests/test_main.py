"""
Test FastAPI application health and endpoints
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
    
    def test_youtube_service_health_endpoint(self):
        """Test YouTube service health endpoint"""
        response = client.get("/api/v1/health/youtube")
        assert response.status_code == 200
        data = response.json()
        assert "service_available" in data
        assert "download_path" in data
        assert "status" in data
    
    def test_network_health_endpoint(self):
        """Test network health endpoint"""
        response = client.get("/api/v1/health/network")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "youtube_domains" in data
        assert "yt_dlp_available" in data
        assert "timestamp" in data


class TestNetworkConnectivity:
    """Test network connectivity for external services"""
    
    def test_youtube_domains_connectivity(self):
        """Test connectivity to YouTube domains"""
        import requests
        
        domains = [
            'https://www.youtube.com',
            'https://youtube.com',
            'https://i.ytimg.com',
        ]
        
        results = []
        for domain in domains:
            try:
                response = requests.get(domain, timeout=10)
                results.append((domain, response.status_code, True))
            except requests.RequestException as e:
                results.append((domain, 0, False))
        
        # At least one domain should be accessible, but skip if none are accessible
        # (This handles cases where YouTube is blocked by firewall/network)
        accessible_domains = [r for r in results if r[2]]
        if len(accessible_domains) == 0:
            pytest.skip("No YouTube domains accessible - likely network/firewall issue")
        
        assert len(accessible_domains) > 0, f"No YouTube domains accessible: {results}"
    
    def test_yt_dlp_basic_functionality(self):
        """Test basic yt-dlp functionality"""
        import yt_dlp
        
        # Test that yt-dlp can be instantiated
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Test basic functionality without downloading
            assert ydl is not None
            assert hasattr(ydl, 'extract_info')


class TestEnvironmentConfiguration:
    """Test environment configuration"""
    
    def test_required_modules_import(self):
        """Test that all required modules can be imported"""
        modules = [
            'fastapi',
            'uvicorn',
            'yt_dlp',
            'moviepy',
            'redis',
            'sqlalchemy',
            'psycopg2',
            'celery',
            'requests',
            'httpx',
        ]
        
        for module_name in modules:
            try:
                __import__(module_name)
            except ImportError as e:
                pytest.fail(f"Required module {module_name} not available: {e}")
    
    def test_upload_directory_creation(self):
        """Test upload directory can be created"""
        import os
        import tempfile
        
        with tempfile.TemporaryDirectory() as tmp_dir:
            upload_dir = os.path.join(tmp_dir, "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            assert os.path.exists(upload_dir)
            assert os.path.isdir(upload_dir)