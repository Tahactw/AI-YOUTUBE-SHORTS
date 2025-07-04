# Security Configuration Guide

## Overview

This document outlines the security measures implemented in the AI YouTube Shorts SaaS application to protect against common web vulnerabilities and ensure secure operation.

## Security Features Implemented

### 1. Secure Configuration Management

- **Environment Variable Validation**: All critical configuration values are validated using Pydantic validators
- **Secret Key Requirements**: Secret keys must be at least 32 characters long and cannot use default values
- **Database URL Validation**: Database connection strings are validated for proper format
- **Environment-Specific Settings**: Different security settings for development, test, and production environments

### 2. Authentication & Authorization

- **Password Hashing**: Uses bcrypt for secure password hashing with salt
- **JWT Token Management**: Secure JWT token creation and verification with configurable expiration
- **Token Validation**: Comprehensive token validation with proper error handling
- **Secret Key Rotation**: Support for secure secret key generation and rotation

### 3. Security Headers

All HTTP responses include security headers:
- **X-Content-Type-Options**: `nosniff` - Prevents MIME type sniffing
- **X-Frame-Options**: `DENY` - Prevents clickjacking attacks
- **X-XSS-Protection**: `1; mode=block` - Enables XSS protection
- **Strict-Transport-Security**: `max-age=31536000; includeSubDomains` - Enforces HTTPS
- **Referrer-Policy**: `strict-origin-when-cross-origin` - Controls referrer information
- **Content-Security-Policy**: `default-src 'self'` - Prevents code injection

### 4. Rate Limiting

- **Request Rate Limiting**: Configurable requests per minute (default: 100)
- **IP-Based Tracking**: Tracks requests by client IP address
- **Automatic Cleanup**: Removes old request records to prevent memory leaks
- **Graceful Degradation**: Returns 429 status with Retry-After header when limit exceeded

### 5. CORS Configuration

- **Origin Validation**: Configurable allowed origins (default: localhost:3000)
- **Method Restrictions**: Configurable allowed HTTP methods
- **Credential Support**: Supports credentials for authenticated requests
- **Production Security**: Stricter CORS policies for production environments

### 6. Session Security

- **Session Middleware**: Secure session management with cryptographic signing
- **Session Cookies**: Secure cookie configuration
- **Session Expiration**: Configurable session timeouts

### 7. Database Security

- **SSL Support**: Configurable SSL requirements for database connections
- **Connection Validation**: Validates database connection strings
- **Environment-Specific Settings**: Different database security settings per environment

## Configuration

### Required Environment Variables

```bash
# Security Configuration - REQUIRED
SECRET_KEY=your-secure-secret-key-minimum-32-characters
JWT_SECRET_KEY=your-secure-jwt-secret-key-minimum-32-characters
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=30
```

### Optional Security Settings

```bash
# CORS Configuration
ALLOWED_ORIGINS=["https://yourdomain.com"]
ALLOWED_METHODS=["GET", "POST", "PUT", "DELETE"]

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# Database Security
DATABASE_SSL_REQUIRE=True

# Redis Security
REDIS_SSL=True
```

## Security Best Practices

### 1. Secret Management

- **Never commit secrets to version control**
- Use the provided secret generation script: `python scripts/generate-secrets.py`
- Rotate secrets regularly in production
- Use environment-specific secrets

### 2. Environment Configuration

- Set `FASTAPI_ENV=production` for production deployments
- Disable debug mode in production: `DEBUG=False`
- Use SSL/TLS for all external connections
- Configure proper database and Redis SSL settings

### 3. Deployment Security

- Use HTTPS in production
- Configure proper firewall rules
- Use trusted host middleware in production
- Implement proper logging and monitoring

### 4. API Security

- All endpoints include security headers
- Rate limiting is applied to all endpoints
- CORS is properly configured
- JWT tokens have reasonable expiration times

## Testing Security

Run the security test suite:

```bash
# Run all security tests
python -m pytest tests/test_security.py tests/test_security_integration.py -v

# Test specific security features
python -m pytest tests/test_security.py::TestSecurityManager -v
python -m pytest tests/test_security_integration.py::TestSecurityIntegration -v
```

## Security Monitoring

### Health Endpoints

- `/api/v1/health` - Basic health check
- `/api/v1/health/network` - Network connectivity check
- `/api/v1/health/youtube` - YouTube service health

### Security Headers Verification

```bash
# Check security headers
curl -I http://localhost:8000/api/v1/health

# Should include all security headers:
# x-content-type-options: nosniff
# x-frame-options: DENY
# x-xss-protection: 1; mode=block
# strict-transport-security: max-age=31536000; includeSubDomains
# referrer-policy: strict-origin-when-cross-origin
# content-security-policy: default-src 'self'
```

## Troubleshooting

### Common Issues

1. **Configuration Validation Errors**
   - Ensure secret keys are at least 32 characters
   - Check database URL format
   - Verify environment variable names

2. **Rate Limiting Issues**
   - Adjust `RATE_LIMIT_REQUESTS` for higher traffic
   - Check client IP detection in load balancer setups
   - Monitor rate limit logs

3. **CORS Issues**
   - Verify `ALLOWED_ORIGINS` configuration
   - Check preflight request handling
   - Ensure credentials are properly configured

### Security Validation

```bash
# Test secret generation
python scripts/generate-secrets.py --secrets-only

# Test configuration validation
python -c "from core.config import get_settings; print(get_settings())"

# Test security features
python -m pytest tests/test_security.py -v
```

## Production Deployment

### Security Checklist

- [ ] Generate secure secrets
- [ ] Configure SSL/TLS certificates
- [ ] Set up proper database SSL
- [ ] Configure Redis SSL
- [ ] Set `FASTAPI_ENV=production`
- [ ] Disable debug mode
- [ ] Configure proper CORS origins
- [ ] Set up monitoring and logging
- [ ] Test all security features
- [ ] Review and update rate limits
- [ ] Configure backup and recovery

### Environment Variables for Production

```bash
# Production Security Settings
FASTAPI_ENV=production
DEBUG=False
SECRET_KEY=<generated-secure-secret>
JWT_SECRET_KEY=<generated-secure-jwt-secret>
DATABASE_SSL_REQUIRE=True
REDIS_SSL=True
ALLOWED_ORIGINS=["https://yourdomain.com"]
RATE_LIMIT_REQUESTS=1000
```

## Support

For security-related issues or questions:
1. Check this documentation
2. Review test cases for examples
3. Run security tests to verify configuration
4. Open an issue in the repository for security concerns

**Note**: For security vulnerabilities, please report them privately to the maintainers.