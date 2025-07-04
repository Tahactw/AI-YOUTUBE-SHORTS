# Frontend - Next.js Application

This directory will contain the Next.js frontend application for the AI YouTube Shorts SaaS.

## Setup Instructions

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **API Client**: Axios
- **UI Components**: shadcn/ui

## Project Structure

```
frontend/
├── app/              # Next.js app directory
├── components/       # Reusable UI components
├── lib/             # Utility functions
├── hooks/           # Custom React hooks
├── types/           # TypeScript type definitions
├── styles/          # Global styles
└── public/          # Static assets
```

## Development Notes

- The frontend will communicate with the FastAPI backend running on port 8000
- CORS is configured on the backend to allow requests from localhost:3000
- Environment variables should be prefixed with `NEXT_PUBLIC_` for client-side access