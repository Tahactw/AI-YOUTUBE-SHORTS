# YouTube Video Testing Configuration

## Overview

This document explains how the YouTube video testing system works in the AI YouTube Shorts application, including the fallback mechanism for handling unavailable videos.

## Problem Statement

The original test configuration used a hardcoded YouTube video ID (`BaW_jenozKc`) that became unavailable, causing CI/CD pipeline failures. To address this, we implemented a robust fallback mechanism that tries multiple video IDs until one succeeds.

## Fallback Video IDs

The application now uses multiple fallback video IDs for testing:

1. **`dQw4w9WgXcQ`** - Rick Astley - Never Gonna Give You Up (very stable)
2. **`9bZkp7q19f0`** - Alternative stable video
3. **`jNQXAC9IVRw`** - Public domain/creative commons video
4. **`BaW_jenozKc`** - Original failing video (kept as fallback)

## Implementation

### YouTube Service Enhancement

The `YouTubeService` class now includes:

#### New Methods

- `get_video_info_with_fallback(video_ids: List[str])` - Tries multiple video IDs until one succeeds
- `download_video_with_fallback(video_ids: List[str])` - Downloads video with fallback mechanism
- `_get_ydl_options(for_download: bool = False)` - Centralized options configuration

#### Enhanced Error Handling

- **Retry Logic**: Configurable retry attempts for network issues
- **Timeout Management**: Proper timeout handling to prevent hanging
- **Detailed Logging**: Comprehensive error messages for debugging
- **Graceful Degradation**: Fallback to next video ID when one fails

### Test Configuration

The test configuration (`tests/conftest.py`) now includes:

```python
# Multiple fallback video IDs for robust testing
FALLBACK_VIDEO_IDS = [
    "dQw4w9WgXcQ",  # Rick Astley - Never Gonna Give You Up (very stable)
    "9bZkp7q19f0",  # Alternative stable video
    "jNQXAC9IVRw",  # Public domain/creative commons video
    "BaW_jenozKc",  # Original failing video (keep as fallback)
]
```

### CI/CD Pipeline Updates

The GitHub Actions workflow now:

1. **Tests Multiple Video IDs**: Tries each fallback video ID in sequence
2. **Handles Failures Gracefully**: Doesn't fail the entire build if YouTube is inaccessible
3. **Provides Detailed Logging**: Shows which video IDs work and which fail
4. **Respects Environment Restrictions**: Acknowledges when YouTube access is blocked

## Usage Examples

### Basic Usage

```python
from services.youtube import YouTubeService

service = YouTubeService()

# Use fallback mechanism
fallback_ids = ['dQw4w9WgXcQ', '9bZkp7q19f0', 'jNQXAC9IVRw']
info = service.get_video_info_with_fallback(fallback_ids)
```

### Download with Fallback

```python
# Download with fallback mechanism
filename = service.download_video_with_fallback(fallback_ids)
```

### Single Video (Original Method)

```python
# Still works for single videos
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
info = service.get_video_info(url)
```

## Testing

### Running Tests

```bash
# Run all YouTube tests
python -m pytest tests/test_youtube.py -v

# Run only fast tests (skip slow network tests)
python -m pytest tests/test_youtube.py -v -m "not slow"

# Run connectivity tests
python test_connectivity.py
```

### Test Categories

1. **Unit Tests**: Mock-based tests that always pass
2. **Integration Tests**: Real YouTube API calls (may be skipped in restricted environments)
3. **Slow Tests**: Marked with `@pytest.mark.slow` for optional execution

## Updating Video IDs

If you need to update the fallback video IDs:

### 1. Update Test Configuration

Edit `tests/conftest.py`:

```python
FALLBACK_VIDEO_IDS = [
    "new_video_id_1",
    "new_video_id_2",
    "new_video_id_3",
    # ... add more as needed
]
```

### 2. Update Service Defaults

Edit `services/youtube.py`:

```python
DEFAULT_FALLBACK_VIDEO_IDS = [
    "new_video_id_1",
    "new_video_id_2",
    "new_video_id_3",
    # ... add more as needed
]
```

### 3. Update CI/CD Pipeline

Edit `.github/workflows/ci.yml` to use the new video IDs in the fallback test section.

## Guidelines for Video ID Selection

When choosing video IDs for testing:

1. **Stability**: Choose videos that are unlikely to be deleted
2. **Availability**: Prefer videos from official channels or public domain
3. **Size**: Use shorter videos for faster testing
4. **Accessibility**: Ensure videos are publicly accessible (not private/unlisted)

### Recommended Sources

- **Official YouTube videos**: Less likely to be removed
- **Creative Commons videos**: Stable and freely available
- **Public domain content**: Safe from copyright issues
- **Popular, well-established videos**: Rick Astley's "Never Gonna Give You Up" is a classic example

## Troubleshooting

### Common Issues

1. **All fallback videos fail**: YouTube access may be restricted in your environment
2. **Tests timeout**: Network connectivity issues or overly long video processing
3. **Video unavailable**: The video ID may have been deleted or made private

### Solutions

1. **Environment Restrictions**: Tests will skip gracefully with proper error messages
2. **Timeout Issues**: Adjust timeout values in `_get_ydl_options()`
3. **Unavailable Videos**: Add the video ID to the fallback list and test locally

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Environment Variables

The service respects these environment variables:

- `UPLOAD_DIR`: Directory for downloaded videos
- `DEBUG`: Enable debug logging
- `YOUTUBE_API_KEY`: YouTube API key (if needed for enhanced functionality)

## Best Practices

1. **Always use fallback mechanism** for production code
2. **Test with multiple video IDs** to ensure robustness
3. **Handle network failures gracefully** with try-catch blocks
4. **Use mocking for unit tests** to avoid network dependencies
5. **Log all failures** for debugging purposes

## Future Enhancements

Potential improvements to consider:

1. **Dynamic video discovery**: Automatically find working videos
2. **Video quality preferences**: Allow specifying preferred video qualities
3. **Caching mechanisms**: Cache successful video IDs for faster testing
4. **Health checking**: Periodically verify video availability
5. **Configuration files**: External configuration for video IDs