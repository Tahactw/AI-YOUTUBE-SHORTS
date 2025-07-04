from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import yt_dlp
from typing import Dict, Any

app = FastAPI(
    title="AI YouTube Shorts SaaS",
    description="A SaaS application for creating AI-powered YouTube Shorts",
    version="1.0.0"
)

# CORS configuration for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI YouTube Shorts SaaS"}

# Network connectivity check endpoint
@app.get("/api/v1/health/network")
async def network_health_check():
    """Network connectivity health check"""
    results = {
        "status": "unknown",
        "youtube_domains": {},
        "yt_dlp_available": False,
        "timestamp": None
    }
    
    # Test YouTube domains
    youtube_domains = [
        "https://www.youtube.com",
        "https://youtube.com",
        "https://i.ytimg.com",
        "https://www.googleapis.com"
    ]
    
    for domain in youtube_domains:
        try:
            response = requests.get(domain, timeout=10)
            results["youtube_domains"][domain] = {
                "accessible": True,
                "status_code": response.status_code
            }
        except Exception as e:
            results["youtube_domains"][domain] = {
                "accessible": False,
                "error": str(e)
            }
    
    # Test yt-dlp availability
    try:
        ydl_opts = {'quiet': True, 'no_warnings': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results["yt_dlp_available"] = True
    except Exception:
        results["yt_dlp_available"] = False
    
    # Determine overall status
    accessible_domains = sum(1 for d in results["youtube_domains"].values() if d["accessible"])
    if accessible_domains > 0 and results["yt_dlp_available"]:
        results["status"] = "healthy"
    elif accessible_domains > 0:
        results["status"] = "partial"
    else:
        results["status"] = "unhealthy"
    
    import datetime
    results["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    return results

# YouTube service test endpoint
@app.get("/api/v1/health/youtube")
async def youtube_service_health():
    """YouTube service health check"""
    try:
        from services.youtube import youtube_service
        
        # Test service initialization
        service_status = {
            "service_available": True,
            "download_path": youtube_service.download_path,
            "download_path_exists": False,
            "status": "healthy"
        }
        
        # Check if download path exists
        import os
        service_status["download_path_exists"] = os.path.exists(youtube_service.download_path)
        
        return service_status
        
    except Exception as e:
        return {
            "service_available": False,
            "error": str(e),
            "status": "unhealthy"
        }

# Include routers
# app.include_router(health_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AI YouTube Shorts SaaS API"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)