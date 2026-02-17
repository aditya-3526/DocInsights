# 🧠 Smart Document Insights

**AI-powered document analysis platform** with semantic search, RAG-based chat, risk detection, and intelligent insights.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green) ![React](https://img.shields.io/badge/React-18-61dafb) ![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- 📄 **Document Upload** — PDF, DOCX, TXT with OCR for scanned documents
- 🔍 **Semantic Search** — AI-powered similarity search across all documents
- 💬 **Chat with Documents** — RAG pipeline with source citations
- 📊 **AI Summarization** — Executive summaries, section highlights, key takeaways
- 🔒 **Risk Detection** — Automated risk scoring and compliance alerts
- 📋 **Key Information Extraction** — Legal, financial, and research-specific extraction
- 📈 **Analytics Dashboard** — Charts, risk distribution, processing status
- ⚖️ **Multi-Document Comparison** — Side-by-side document analysis

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy, Python 3.11 |
| AI/ML | LangChain, SentenceTransformers, FAISS |
| Frontend | React 18, TailwindCSS, Recharts |
| Workers | Celery + Redis |
| Database | SQLite (dev) / PostgreSQL (prod) |

## Quick Start

### 1. Clone & Setup

```bash
cd smart-document-insights
cp .env.example .env
# Edit .env and set your OPENAI_API_KEY (optional — runs in demo mode without it)
```

### 2. Install Backend

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### 3. Start Backend

```bash
uvicorn backend.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### 4. Install & Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: http://localhost:5173

### 5. (Optional) Start Celery Worker

```bash
# Requires Redis running on localhost:6379
celery -A backend.workers.celery_app worker --loglevel=info
```

## Docker Deployment

```bash
cp .env.example .env
# Edit .env with your settings
docker-compose up --build
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Cloud Deployment

### Render
1. Create a Web Service pointing to the repo
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env.example`

### Railway / Fly.io
Use the provided `Dockerfile.backend` and `docker-compose.yml`

### AWS
- **ECS/Fargate**: Use Docker images
- **Lambda**: Wrap with Mangum adapter
- **S3**: Set `UPLOAD_DIR` to S3 bucket path

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for LLM features | — |
| `OPENAI_MODEL` | LLM model name | gpt-3.5-turbo |
| `DATABASE_URL` | Database connection string | sqlite (local) |
| `REDIS_URL` | Redis URL for Celery | redis://localhost:6379/0 |
| `MAX_FILE_SIZE_MB` | Upload size limit | 50 |
| `EMBEDDING_MODEL` | SentenceTransformer model | all-MiniLM-L6-v2 |

## Testing

```bash
python -m pytest tests/ -v
```

## Architecture

```
Backend (FastAPI) → Services → AI Layer (LangChain + FAISS)
     ↕                              ↕
  Database (SQLAlchemy)    Vector Store (FAISS)
     ↕
Celery Workers → Redis
```

## License

MIT
