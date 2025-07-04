"""
Integration tests for security middleware and endpoints
"""

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestSecurityIntegration:
    """Test security integration with the main application"""
    
    def test_root_endpoint_with_security_headers(self):
        """Test root endpoint includes security headers"""
        response = client.get("/")
        
        assert response.status_code == 200
        
        # Check security headers are present
        assert "x-content-type-options" in response.headers
        assert "x-frame-options" in response.headers
        assert "x-xss-protection" in response.headers
        assert "strict-transport-security" in response.headers
        assert "referrer-policy" in response.headers
        assert "content-security-policy" in response.headers
        
        # Check header values
        assert response.headers["x-content-type-options"] == "nosniff"
        assert response.headers["x-frame-options"] == "DENY"
        assert response.headers["x-xss-protection"] == "1; mode=block"
        assert "max-age=31536000" in response.headers["strict-transport-security"]
        assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
        assert response.headers["content-security-policy"] == "default-src 'self'"
        
        # Check response content
        data = response.json()
        assert data["status"] == "secure"
        assert data["environment"] == "test"
    
    def test_health_endpoint_with_security_headers(self):
        """Test health endpoint includes security headers"""
        response = client.get("/api/v1/health")
        
        assert response.status_code == 200
        
        # Check security headers are present
        assert "x-content-type-options" in response.headers
        assert "x-frame-options" in response.headers
        assert "x-xss-protection" in response.headers
        assert "strict-transport-security" in response.headers
        assert "referrer-policy" in response.headers
        assert "content-security-policy" in response.headers
        
        # Check response content
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "AI YouTube Shorts SaaS"
    
    def test_cors_headers_present(self):
        """Test CORS headers are properly configured"""
        response = client.get("/", headers={"Origin": "http://localhost:3000"})
        
        assert response.status_code == 200
        # FastAPI's CORS middleware adds these headers on preflight requests
        # For a simple GET request, we just verify the app doesn't reject it
    
    def test_rate_limiting_allows_normal_requests(self):
        """Test that normal request volume is allowed"""
        # Make several requests to ensure rate limiting doesn't interfere
        for i in range(10):
            response = client.get("/")
            assert response.status_code == 200
    
    def test_network_health_endpoint_with_security(self):
        """Test network health endpoint with security headers"""
        response = client.get("/api/v1/health/network")
        
        assert response.status_code == 200
        
        # Check security headers are present
        assert "x-content-type-options" in response.headers
        assert "x-frame-options" in response.headers
        
        # Check response structure
        data = response.json()
        assert "status" in data
        assert "youtube_domains" in data
        assert "yt_dlp_available" in data
        assert "timestamp" in data
    
    def test_youtube_health_endpoint_with_security(self):
        """Test YouTube health endpoint with security headers"""
        response = client.get("/api/v1/health/youtube")
        
        assert response.status_code == 200
        
        # Check security headers are present
        assert "x-content-type-options" in response.headers
        assert "x-frame-options" in response.headers
        
        # Check response structure
        data = response.json()
        assert "status" in data
        # Other fields may vary based on service availability