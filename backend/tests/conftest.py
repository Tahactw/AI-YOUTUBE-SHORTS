"""
Test configuration for backend tests
"""
import pytest
import os
from pathlib import Path

# Test configuration
TEST_UPLOAD_DIR = "test_uploads"

# Multiple fallback video IDs for robust testing
FALLBACK_VIDEO_IDS = [
    "dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up (very stable)
    "9bZkp7q19f0",  # Alternative stable video
    "jNQXAC9IVRw",  # Public domain/creative commons video
    "BaW_jenozKc",  # Original failing video (keep as fallback)
]

# Generate fallback YouTube URLs
FALLBACK_YOUTUBE_URLS = [f"https://www.youtube.com/watch?v={vid}" for vid in FALLBACK_VIDEO_IDS]
TEST_YOUTUBE_URL = FALLBACK_YOUTUBE_URLS[0]  # Default to first fallback

@pytest.fixture(scope="session")
def test_upload_dir():
    """Create test upload directory"""
    upload_dir = Path(TEST_UPLOAD_DIR)
    upload_dir.mkdir(exist_ok=True)
    yield upload_dir
    # Cleanup after tests
    import shutil
    if upload_dir.exists():
        shutil.rmtree(upload_dir)

@pytest.fixture
def test_youtube_url():
    """Test YouTube URL"""
    return TEST_YOUTUBE_URL

@pytest.fixture
def fallback_youtube_urls():
    """Fallback YouTube URLs for testing"""
    return FALLBACK_YOUTUBE_URLS

@pytest.fixture
def fallback_video_ids():
    """Fallback video IDs for testing"""
    return FALLBACK_VIDEO_IDS