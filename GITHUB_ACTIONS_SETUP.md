# GitHub Actions CI/CD Configuration

This document explains the GitHub Actions configuration for the AI YouTube Shorts SaaS project, specifically addressing YouTube access and network connectivity issues.

## Overview

The GitHub Actions workflow (`/.github/workflows/ci.yml`) is designed to:
- Set up a proper environment for YouTube access
- Configure network connectivity for YouTube domains
- Install and test all dependencies including yt-dlp
- Provide comprehensive testing for YouTube functionality
- Handle firewall and network access issues

## Workflow Structure

### 1. Setup Job
- **Purpose**: Initialize the environment and install dependencies
- **Key Actions**:
  - Install Python 3.11+ with pip
  - Install system dependencies (ffmpeg, git, curl)
  - Install Python dependencies from requirements.txt
  - Create necessary directories
  - Test basic functionality

### 2. Test Job
- **Purpose**: Run comprehensive tests including network connectivity
- **Key Actions**:
  - Test YouTube domain accessibility
  - Test yt-dlp functionality with real YouTube video
  - Test FastAPI application health endpoints
  - Run backend tests with pytest
  - Verify YouTube service integration

### 3. Build Job
- **Purpose**: Verify application builds correctly
- **Key Actions**:
  - Build backend application
  - Test Docker container builds
  - Verify container functionality

### 4. Deploy Job
- **Purpose**: Deployment placeholder for future use
- **Key Actions**:
  - Placeholder for production deployment
  - Environment-specific deployment steps

## Network Configuration

### YouTube Domain Access

The workflow tests connectivity to these YouTube domains:
- `www.youtube.com` - Main YouTube website
- `youtube.com` - YouTube redirect domain
- `i.ytimg.com` - YouTube image assets
- `www.googleapis.com` - Google APIs

### Firewall Configuration

GitHub Actions runners have internet access by default, but the workflow includes:
- Timeout configurations for network requests
- Retry logic for failed connections
- Fallback mechanisms for network issues
- Comprehensive error reporting

## Environment Variables

The workflow configures these environment variables:

```yaml
FASTAPI_ENV: test
DEBUG: True
SECRET_KEY: test-secret-key
JWT_SECRET_KEY: test-jwt-secret-key
DATABASE_URL: postgresql://postgres:postgres@localhost:5432/ai_youtube_shorts_test
REDIS_URL: redis://localhost:6379
UPLOAD_DIR: uploads
MAX_UPLOAD_SIZE: 104857600
CELERY_BROKER_URL: redis://localhost:6379
CELERY_RESULT_BACKEND: redis://localhost:6379
```

## System Dependencies

The workflow installs these system dependencies:
- `ffmpeg` - For video processing
- `git` - For version control
- `curl` - For network testing
- Python 3.11+ - Runtime environment

## Testing Strategy

### Network Connectivity Tests
- Basic internet connectivity verification
- YouTube domain accessibility testing
- yt-dlp functionality testing
- API health endpoint testing

### YouTube Service Tests
- Service initialization testing
- Video information extraction testing
- Download functionality testing (with mocks)
- Error handling testing

### Application Tests
- FastAPI application testing
- Health endpoint testing
- Environment configuration testing
- Dependency verification

## Local Development

### Prerequisites
- Docker and Docker Compose
- Python 3.11+
- Internet access for YouTube domains

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Tahactw/AI-YOUTUBE-SHORTS.git
   cd AI-YOUTUBE-SHORTS
   ```

2. **Environment setup**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Development with Docker** (recommended):
   ```bash
   # Start all services
   docker-compose up -d
   
   # View logs
   docker-compose logs -f
   
   # Stop services
   docker-compose down
   ```

4. **Network connectivity testing**:
   ```bash
   # Test network with Docker
   docker-compose --profile test run network-test
   
   # Test locally
   cd backend
   python test_connectivity.py
   ```

### Health Endpoints

The application provides these health check endpoints:

- **Basic Health**: `GET /api/v1/health`
  - Returns basic application health status

- **Network Health**: `GET /api/v1/health/network`
  - Tests YouTube domain connectivity
  - Verifies yt-dlp availability
  - Returns detailed network status

- **YouTube Service Health**: `GET /api/v1/health/youtube`
  - Tests YouTube service initialization
  - Verifies download path configuration
  - Returns service status

### Example Health Check Response

```json
{
  "status": "unhealthy",
  "youtube_domains": {
    "https://www.youtube.com": {
      "accessible": false,
      "error": "Connection timeout"
    },
    "https://youtube.com": {
      "accessible": true,
      "status_code": 200
    }
  },
  "yt_dlp_available": true,
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

## Troubleshooting

### Common Issues

1. **YouTube domains not accessible**:
   - Check firewall settings
   - Verify DNS resolution
   - Test with different networks

2. **yt-dlp extraction failures**:
   - Update yt-dlp to latest version
   - Check user agent configuration
   - Verify YouTube URL format

3. **Docker network issues**:
   - Restart Docker service
   - Check network bridge configuration
   - Verify container network settings

### Debug Commands

```bash
# Test network connectivity
curl -v https://www.youtube.com

# Test yt-dlp directly
yt-dlp --version
yt-dlp --list-formats "https://www.youtube.com/watch?v=BaW_jenozKc"

# Test backend health
curl http://localhost:8000/api/v1/health/network

# Run connectivity test script
cd backend
python test_connectivity.py
```

## Security Considerations

### Network Security
- All network requests use HTTPS
- Timeout configurations prevent hanging requests
- Error handling prevents information leakage
- User agent strings are configured appropriately

### Environment Security
- Test environment uses separate credentials
- Production secrets are not exposed in CI
- Database isolation for testing
- Temporary file cleanup

## Performance Optimization

### Network Optimization
- Connection pooling for HTTP requests
- Timeout configurations for responsiveness
- Retry logic for transient failures
- Parallel testing where possible

### Build Optimization
- Dependency caching
- Docker layer caching
- Incremental builds
- Parallel job execution

## Monitoring and Logging

### CI/CD Monitoring
- Build status notifications
- Test result reporting
- Performance metrics
- Error tracking

### Application Monitoring
- Health endpoint monitoring
- Network connectivity tracking
- Service availability metrics
- Error rate monitoring

## Future Enhancements

### Planned Features
- Production deployment automation
- Performance testing integration
- Security scanning
- Load testing capabilities

### Network Enhancements
- CDN integration for video assets
- Regional deployment support
- Network optimization
- Bandwidth management

## Support

For issues related to GitHub Actions or YouTube access:
1. Check the workflow logs in GitHub Actions
2. Review the health endpoint responses
3. Run the connectivity test script locally
4. Check the troubleshooting section above

For additional support, please open an issue in the repository.