#!/bin/bash
# setup-env.sh - Environment setup script for AI YouTube Shorts SaaS

echo "🔧 Setting up secure environment for AI YouTube Shorts SaaS..."

# Create backend directory if it doesn't exist
mkdir -p backend/uploads

# Generate secure secrets
echo "🔐 Generating secure secrets..."
python scripts/generate-secrets.py

# Create uploads directory with proper permissions
echo "📁 Creating uploads directory..."
mkdir -p backend/uploads
chmod 755 backend/uploads

# Set proper permissions on .env file
if [ -f backend/.env ]; then
    echo "🔒 Setting secure permissions on .env file..."
    chmod 600 backend/.env
fi

echo "✅ Environment setup complete!"
echo ""
echo "⚠️  Remember to:"
echo "   1. Update API keys in backend/.env"
echo "   2. Configure production database settings"
echo "   3. Never commit .env to version control"
echo "   4. Review security settings before deployment"
echo ""
echo "🚀 To start the application:"
echo "   cd backend"
echo "   pip install -r requirements.txt"
echo "   uvicorn main:app --reload"
echo ""
echo "📚 Documentation:"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - Health Check: http://localhost:8000/api/v1/health"
echo "   - Security: All endpoints include security headers"