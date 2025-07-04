#!/usr/bin/env python3
"""
Script to generate secure secrets for the application
"""

import secrets
import os
import sys
from pathlib import Path

def generate_env_file():
    """Generate .env file with secure secrets"""
    
    print("🔧 Generating secure environment variables...")
    
    # Generate secure secrets
    secret_key = secrets.token_urlsafe(32)
    jwt_secret = secrets.token_urlsafe(32)
    
    # Get the backend directory
    backend_dir = Path(__file__).parent.parent / "backend"
    env_file = backend_dir / ".env"
    
    # Create env content
    env_content = f"""# Generated secrets - DO NOT COMMIT TO VERSION CONTROL
SECRET_KEY={secret_key}
JWT_SECRET_KEY={jwt_secret}

# Environment
FASTAPI_ENV=development
DEBUG=True

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_youtube_shorts
DATABASE_SSL_REQUIRE=False

# Redis
REDIS_URL=redis://localhost:6379
REDIS_SSL=False

# CORS
ALLOWED_ORIGINS=["http://localhost:3000"]

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# File Upload
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE=104857600

# External APIs
OPENAI_API_KEY=your-openai-key-here
YOUTUBE_API_KEY=your-youtube-key-here

# Celery
CELERY_BROKER_URL=redis://localhost:6379
CELERY_RESULT_BACKEND=redis://localhost:6379
"""
    
    # Write the file
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        # Set proper permissions
        os.chmod(env_file, 0o600)
        
        print("✅ Generated .env file with secure secrets")
        print(f"📁 Location: {env_file}")
        print("⚠️  Remember to:")
        print("   1. Update API keys in .env")
        print("   2. Configure production database settings")
        print("   3. Never commit .env to version control")
        print("🔒 File permissions set to 600 (owner read/write only)")
        
    except Exception as e:
        print(f"❌ Error generating .env file: {e}")
        sys.exit(1)


def generate_secrets_only():
    """Generate only the secrets and print them"""
    
    print("🔐 Generating secure secrets:")
    print(f"SECRET_KEY={secrets.token_urlsafe(32)}")
    print(f"JWT_SECRET_KEY={secrets.token_urlsafe(32)}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--secrets-only":
        generate_secrets_only()
    else:
        generate_env_file()