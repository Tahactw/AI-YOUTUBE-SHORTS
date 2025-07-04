"""
Test configuration for backend tests
"""
import pytest
import os
from pathlib import Path

# Test configuration
TEST_UPLOAD_DIR = "test_uploads"
TEST_YOUTUBE_URL = "https://www.youtube.com/watch?v=BaW_jenozKc"  # Short test video

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