"""
Security middleware for FastAPI application
"""

import time
from typing import Dict, List
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to add security headers to all responses"""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple rate limiting middleware"""
    
    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[float]] = {}
    
    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Clean old requests (older than 1 minute)
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if current_time - req_time < 60
            ]
        
        # Initialize if not exists
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded",
                headers={"Retry-After": "60"}
            )
        
        # Add current request
        self.requests[client_ip].append(current_time)
        
        response = await call_next(request)
        return response


def add_security_middleware(app: FastAPI, settings) -> None:
    """Add all security middleware to the FastAPI app"""
    
    # Add security headers
    app.add_middleware(SecurityHeadersMiddleware)
    
    # Add rate limiting
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=getattr(settings, 'rate_limit_requests', 100)
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=getattr(settings, 'allowed_origins', ["http://localhost:3000"]),
        allow_credentials=True,
        allow_methods=getattr(settings, 'allowed_methods', ["GET", "POST", "PUT", "DELETE"]),
        allow_headers=["*"],
    )
    
    # Add trusted hosts for production
    if getattr(settings, 'fastapi_env', 'development') == "production":
        app.add_middleware(
            TrustedHostMiddleware,
            allowed_hosts=getattr(settings, 'allowed_origins', ["*"])
        )
    
    # Add session middleware
    app.add_middleware(
        SessionMiddleware,
        secret_key=getattr(settings, 'secret_key', 'fallback-secret-key')
    )