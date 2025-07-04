# YouTube Download API Documentation

## Overview
The YouTube Download API provides endpoints to download YouTube videos, extract metadata, and track download progress.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, no authentication is required for the API endpoints (development mode).

## Endpoints

### 1. Download YouTube Video
**POST** `/api/v1/youtube/download`

Download a YouTube video and return a job ID for tracking.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "pending",
  "message": "Download started successfully",
  "created_at": "2024-01-01T12:00:00.000000",
  "metadata": {
    "title": "Video Title",
    "description": "Video description",
    "duration": 180,
    "thumbnail": "https://example.com/thumbnail.jpg",
    "uploader": "Channel Name",
    "view_count": 1000000,
    "upload_date": "20240101"
  },
  "file_path": null,
  "error_details": null
}
```

### 2. Get Download Status
**GET** `/api/v1/youtube/download/{job_id}/status`

Get the status of a download job.

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "completed",
  "progress": null,
  "message": "Download completed",
  "file_path": "downloads/video_file.mp4",
  "error_details": null
}
```

### 3. Get Video Metadata
**POST** `/api/v1/youtube/metadata`

Get video metadata without downloading.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response:**
```json
{
  "success": true,
  "metadata": {
    "title": "Video Title",
    "description": "Video description",
    "duration": 180,
    "thumbnail": "https://example.com/thumbnail.jpg",
    "uploader": "Channel Name",
    "view_count": 1000000,
    "upload_date": "20240101"
  },
  "error": null
}
```

### 4. List All Jobs
**GET** `/api/v1/youtube/jobs`

List all download jobs.

**Response:**
```json
{
  "total_jobs": 1,
  "jobs": {
    "uuid-string": {
      "status": "completed",
      "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "metadata": { ... },
      "created_at": "2024-01-01T12:00:00.000000",
      "file_path": "downloads/video_file.mp4"
    }
  }
}
```

### 5. Cancel Job
**DELETE** `/api/v1/youtube/jobs/{job_id}`

Cancel a download job.

**Response:**
```json
{
  "message": "Job cancelled successfully"
}
```

### 6. Test Mode Management
**POST** `/api/v1/youtube/test-mode?enable={true|false}`

Toggle test mode for development/testing.

**GET** `/api/v1/youtube/test-mode`

Get current test mode status.

### 7. Health Check
**GET** `/api/v1/health`

Check API health status.

## Status Values
- `pending`: Download has been queued
- `in_progress`: Download is currently in progress
- `completed`: Download has completed successfully
- `failed`: Download has failed

## Error Handling
The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid URL, etc.)
- `404`: Job not found
- `422`: Validation error
- `500`: Internal server error

## URL Validation
Supported YouTube URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://m.youtube.com/watch?v=VIDEO_ID`

## Configuration
The API respects the following configuration limits:
- Maximum file size: 500MB
- Maximum video duration: 1 hour
- Allowed formats: mp4, webm, mkv
- Download timeout: 5 minutes

## Development Mode
In test mode, the API returns mock data instead of actually downloading videos from YouTube. This is useful for development and testing without hitting YouTube's servers.

## API Documentation
Interactive API documentation is available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`