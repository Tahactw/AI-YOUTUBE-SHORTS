from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from api.health import router as health_router
# import uvicorn

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

# Include routers
# app.include_router(health_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "AI YouTube Shorts SaaS API"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)