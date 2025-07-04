# AI YouTube Shorts SaaS

A comprehensive SaaS application for creating AI-powered YouTube Shorts with automated transcription, video processing, and content generation.

## Features

- 🎥 YouTube video download and processing
- 🎙️ AI-powered transcription using OpenAI Whisper
- ✂️ Automated video editing and shorts creation
- 🤖 AI-generated content and captions
- 📊 Analytics and performance tracking
- 💼 Multi-tenant SaaS architecture
- 🚀 Scalable background processing with Celery

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.9+
- **Database**: PostgreSQL
- **Cache**: Redis
- **Background Tasks**: Celery
- **AI/ML**: OpenAI Whisper, MoviePy
- **Video Processing**: yt-dlp, MoviePy

### Frontend
- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **UI Components**: shadcn/ui

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Deployment**: AWS/GCP (planned)
- **CI/CD**: GitHub Actions (planned)

## Project Structure

```
AI-YOUTUBE-SHORTS/
├── backend/                 # FastAPI backend application
│   ├── api/                # API routes
│   ├── core/               # Core functionality
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   ├── main.py            # FastAPI app entry point
│   └── requirements.txt   # Python dependencies
├── frontend/              # Next.js frontend application
│   └── README.md         # Frontend setup instructions
├── docker-compose.yml    # Docker services configuration
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
└── README.md           # This file
```

## Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Tahactw/AI-YOUTUBE-SHORTS.git
cd AI-YOUTUBE-SHORTS
```

### 2. Environment Setup

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# Add your OpenAI API key, YouTube API key, etc.
```

### 3. Docker Development (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

The application will be available at:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs

### 4. Manual Development Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --reload
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### External Services

```bash
# Start Redis
docker run -d -p 6379:6379 redis:7-alpine

# Start PostgreSQL
docker run -d -p 5432:5432 -e POSTGRES_DB=ai_youtube_shorts -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres postgres:15-alpine

# Start Celery worker
cd backend
celery -A main.celery worker --loglevel=info
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

### Adding New Features

1. **Backend**: Add new API endpoints in `backend/api/`
2. **Frontend**: Add new pages/components in `frontend/`
3. **Models**: Define data models in `backend/models/`
4. **Services**: Implement business logic in `backend/services/`

### Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Code Quality

```bash
# Backend linting
cd backend
flake8 .
black .

# Frontend linting
cd frontend
npm run lint
npm run type-check
```

## Deployment

### Production Build

```bash
# Build all services
docker-compose -f docker-compose.prod.yml build

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

### Environment Variables

Key environment variables to configure:

- `OPENAI_API_KEY`: OpenAI API key for Whisper transcription
- `YOUTUBE_API_KEY`: YouTube Data API key
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: FastAPI secret key
- `JWT_SECRET_KEY`: JWT signing key

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue on GitHub or contact the maintainers.

---

**Note**: This is a SaaS application. Please ensure you comply with YouTube's Terms of Service and API usage policies when using this application.