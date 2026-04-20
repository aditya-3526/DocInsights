<p align="center">
  <img src="docs/dashboard-with-data.png" alt="DocInsights Dashboard" width="100%"/>
</p>

<h1 align="center">⚡ DocInsights — AI Document Intelligence Platform</h1>

<p align="center">
  <strong>Upload documents. Ask questions. Get AI-powered insights in seconds.</strong>
</p>

<p align="center">
  <a href="#-problem-statement">🎯 Why</a> •
  <a href="#-features">✨ Features</a> •
  <a href="#-whats-new-v2">🆕 What's New</a> •
  <a href="#-demo-walkthrough">🎬 Demo</a> •
  <a href="#-quick-start">🚀 Quick Start</a> •
  <a href="#-architecture">🏗 Architecture</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React"/>
  <img src="https://img.shields.io/badge/Tailwind-3.4-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white" alt="Tailwind"/>
  <img src="https://img.shields.io/badge/FAISS-Vector_Search-FF6F00?style=for-the-badge" alt="FAISS"/>
  <img src="https://img.shields.io/badge/RAG-Pipeline-8B5CF6?style=for-the-badge" alt="RAG"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
</p>

---

## 🎯 Problem Statement

Professionals routinely deal with **hundreds of documents** — contracts, research papers, reports, compliance filings — yet extracting actionable insights from them remains painfully manual.

**DocInsights** solves this by providing an **AI-powered document intelligence platform** that can:

- **Understand** any document through semantic analysis
- **Answer questions** with source-cited, explainable responses (RAG)
- **Detect risks** automatically with severity scoring
- **Compare** multiple documents side-by-side with AI-generated analysis
- **Generate reports** as downloadable PDFs with executive summaries

> **Think of it as ChatGPT for your documents — but with full transparency into *where* every answer comes from.**

---

## ✨ Features

### 📄 Document Management
- **Multi-format upload** — PDF, DOCX, TXT with drag-and-drop
- **Real-time processing pipeline** — uploading → chunking → embedding → ready
- **Smart text extraction** with OCR fallback (Tesseract)

### 🔍 Semantic Search
- **AI-powered similarity search** across all documents using FAISS
- **Auto-scaling index** — flat index → IVF at 256+ vectors
- **Relevance scoring** with visual confidence bars

### 💬 Chat with Documents (RAG)
- **Retrieval-Augmented Generation** — grounded answers with source citations
- **Context-aware conversations** — full chat history per document
- **Source transparency** — see exactly which chunks informed each answer

### 📊 AI-Powered Insights
- **Executive summaries** with key takeaways
- **Risk detection** — automated severity scoring (High / Medium / Low)
- **Key information extraction** — dates, parties, clauses, financials

### ⚖️ Multi-Document Comparison
- **Side-by-side analysis** of up to 5 documents
- **AI-generated diff** — similarities and differences highlighted automatically

### 📈 Analytics Dashboard
- **Animated stat cards** — document count, risk totals, severity breakdown
- **Interactive charts** — document types donut, risk distribution bars
- **Pipeline status** for all documents in the system

---

## 🆕 What's New (v2)

Three major features added in the latest release, all production-safe and backward-compatible:

### 🔦 Explainable AI — Evidence Highlighting

Every AI answer now includes **clickable evidence highlights** showing exactly which text was used to generate the response.

- **Rich metadata**: exact text, page number, character offsets, relevance score
- **Click-to-navigate**: clicking a highlight opens the document and **scrolls to the exact text**
- **Visual highlighting**: the source text is wrapped in an amber `<mark>` for instant identification
- **"Clear Highlight"** button to dismiss

> **User flow**: Ask question → See evidence → Click highlight → Document opens → Auto-scrolls → Text is highlighted

<!-- Screenshots: chat highlight + document highlight -->

### 📄 AI Report Generator

Generate **comprehensive PDF reports** for any document with a single click.

- **Smart caching**: reuses existing insights from the database — no redundant LLM calls
- **90-second timeout budget** with per-step guards
- **Graceful degradation**: if any section fails, the report still generates with available data
- **Sections**: Executive Summary, Key Highlights, Risk Analysis, Extracted Information
- **Download**: streams as PDF directly to the browser

### 📊 Multi-Document Chat

Chat **across multiple documents simultaneously** with cross-document source attribution.

- **Select 2–5 documents** and ask questions that span all of them
- **Bounded retrieval**: `min(top_k × 3, 50)` cap prevents performance degradation
- **Per-document chunk limits** (max 3/doc) + deduplication + re-ranking
- **Token-aware context**: 6,000-token budget with round-robin document balancing
- **Grouped sources**: responses show sources organized by document

### 🛡️ Production Safety (Cross-Cutting)

- **`safe_llm_call()`** — all LLM calls wrapped with configurable timeout (15–20s) + fallback response
- **Feature flags** — each feature independently toggleable via environment variables
- **Bounded FAISS over-fetch** — hard cap of 50 vectors per search
- **Comprehensive observability** — `structlog` events with latency tracking for embed/retrieve/LLM

---

## 🎬 Demo Walkthrough

Follow these steps to see all features in action:

```
Step 1: Upload a Document
    → Go to Documents tab → Drag & drop any PDF/DOCX/TXT
    → Watch the real-time processing pipeline

Step 2: Generate AI Insights
    → Open the document → Click "Summarize", "Risk Analysis", or "Extract Info"
    → View results in the Insights tab

Step 3: Chat with Your Document
    → Click "Chat" → Ask any question about the document
    → See source-cited answers with relevance scores

Step 4: Click on Evidence Highlights
    → In the chat, scroll to the "Evidence" section
    → Click any highlight → Document opens → Scrolls to exact text

Step 5: Generate a PDF Report
    → On the document page → Click "Generate Report"
    → PDF downloads automatically with summary, risks, and extracted data

Step 6: Multi-Document Chat
    → Go to "Multi-Chat" in the sidebar
    → Select 2–5 documents → Ask a cross-document question
    → See sources grouped by document

Step 7: Search & Compare
    → Use Semantic Search to find relevant content across all docs
    → Use Compare to analyze multiple documents side-by-side
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- An OpenAI-compatible API key (e.g., [OpenRouter](https://openrouter.ai))

### 1. Clone & Configure

```bash
git clone https://github.com/aditya-3526/DocInsights.git
cd DocInsights
cp .env.example .env
```

Edit `.env` and set your API key:
```env
OPENAI_API_KEY=your-api-key-here
OPENAI_API_BASE=https://openrouter.ai/api/v1
OPENAI_MODEL=openai/gpt-3.5-turbo
```

### 2. Backend Setup

```bash
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

API docs at: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

App running at: [http://localhost:5173](http://localhost:5173)

### 4. (Optional) Celery Workers

```bash
# Requires Redis on localhost:6379
celery -A backend.workers.celery_app worker --loglevel=info
```

> **Note**: If Redis isn't running, document processing happens inline automatically — no setup needed.

---

## 🛠 Tech Stack

### Backend
| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI with async SQLAlchemy |
| **LLM** | OpenRouter / OpenAI (GPT-3.5-turbo) |
| **LLM Safety** | `safe_llm_call()` — timeout + fallback wrapper |
| **Embeddings** | SentenceTransformers (`all-MiniLM-L6-v2`) |
| **Vector Store** | FAISS (auto-upgrades flat → IVF at 256+ vectors) |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **PDF Generation** | fpdf2 |
| **Workers** | Celery + Redis (optional — falls back to inline) |
| **Caching** | In-memory LRU (LLM responses + query embeddings) |
| **Logging** | structlog (structured JSON events) |

### Frontend
| Component | Technology |
|-----------|-----------|
| **Framework** | React 18 + Vite |
| **Styling** | Tailwind CSS with custom design system |
| **Charts** | Recharts |
| **Icons** | Lucide React |
| **HTTP Client** | Axios |
| **Routing** | React Router v6 |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React)                         │
│  React 18 + Vite + Tailwind CSS                                  │
│  Pages: Dashboard, Documents, Chat, Multi-Chat, Search, Compare  │
│  /api/* → reverse proxy to backend                               │
└──────────────────────────┬───────────────────────────────────────┘
                           │ HTTPS / localhost
┌──────────────────────────▼───────────────────────────────────────┐
│                        Backend (FastAPI)                          │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  API Layer                                                 │   │
│  │  ├── documents.py    → Upload, list, delete, get           │   │
│  │  ├── chat.py         → RAG chat (single doc + highlights)  │   │
│  │  ├── chat_v2.py      → Multi-doc chat (2–5 documents)      │   │
│  │  ├── report.py       → PDF report generation               │   │
│  │  ├── search.py       → Semantic search                     │   │
│  │  ├── compare.py      → Multi-doc comparison                │   │
│  │  ├── insights.py     → Summarize, extract, risk detection  │   │
│  │  └── dashboard.py    → Analytics & stats                   │   │
│  ├────────────────────────────────────────────────────────────┤   │
│  │  Service Layer                                             │   │
│  │  ├── llm_client.py        → LLM + safe_llm_call() wrapper │   │
│  │  ├── rag_service.py       → RAG pipeline + highlights      │   │
│  │  ├── rag_service_v2.py    → Multi-doc RAG (isolated)       │   │
│  │  ├── report_service.py    → PDF generation + caching       │   │
│  │  ├── vector_store.py      → FAISS (bounded over-fetch)     │   │
│  │  ├── embedding_service.py → Query embedding + cache        │   │
│  │  └── document_processor.py → Text extraction               │   │
│  ├────────────────────────────────────────────────────────────┤   │
│  │  Data Layer                                                │   │
│  │  ├── SQLite/PostgreSQL (docs, chunks, insights, chat)      │   │
│  │  ├── FAISS Index (vector embeddings for search)            │   │
│  │  └── LLM (OpenRouter / OpenAI API)                         │   │
│  └────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### RAG Pipeline (Single Document)
```
Question → Embed Query → FAISS Search → Retrieve Top-K Chunks
    → Build Context → safe_llm_call(prompt, timeout=15s)
    → Parse Answer → Build Highlights → Return {answer, sources, highlights}
```

### Multi-Document RAG Pipeline
```
Question → Embed Query → FAISS Global Search (bounded: min(k×3, 50))
    → Filter by doc_ids → Deduplicate → Per-doc cap (3/doc)
    → Re-rank by score → Token-aware round-robin context (6000 tokens)
    → safe_llm_call(prompt, timeout=20s)
    → Return {answer, sources, highlights, document_groups}
```

---

## 📁 Project Structure

```
DocInsights/
├── backend/
│   ├── api/                     # REST API endpoints
│   │   ├── documents.py         # Upload, list, delete, get document
│   │   ├── chat.py              # RAG chat with highlights
│   │   ├── chat_v2.py           # Multi-document chat (NEW)
│   │   ├── report.py            # PDF report generation (NEW)
│   │   ├── search.py            # Semantic search
│   │   ├── compare.py           # Multi-document comparison
│   │   ├── insights.py          # Summarize, extract, risk detection
│   │   └── dashboard.py         # Analytics & stats
│   ├── services/                # Business logic layer
│   │   ├── llm_client.py        # LLM wrapper + safe_llm_call()
│   │   ├── rag_service.py       # RAG pipeline + highlight extraction
│   │   ├── rag_service_v2.py    # Multi-doc RAG pipeline (NEW)
│   │   ├── report_service.py    # PDF generation service (NEW)
│   │   ├── vector_store.py      # FAISS index (bounded over-fetch)
│   │   ├── embedding_service.py # Embeddings with query cache
│   │   ├── document_processor.py # PDF/DOCX/TXT text extraction
│   │   ├── prompts.py           # Centralized prompt templates
│   │   └── response_parser.py   # JSON parsing + validators
│   ├── models/                  # SQLAlchemy models + Pydantic schemas
│   ├── utils/                   # Text processing, file validation
│   ├── workers/                 # Celery background tasks (optional)
│   ├── config.py                # App config + feature flags
│   ├── database.py              # Async database engine & sessions
│   └── main.py                  # FastAPI app entry point
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI components
│   │   │   ├── ui.jsx           # AnimatedCounter, StatusBadge, Skeleton
│   │   │   └── Toast.jsx        # Toast notification system
│   │   ├── pages/               # Page components
│   │   │   ├── DashboardPage.jsx    # Analytics dashboard
│   │   │   ├── UploadPage.jsx       # Document upload & list
│   │   │   ├── DocumentPage.jsx     # Doc viewer + highlight scroll
│   │   │   ├── ChatPage.jsx         # Single-doc RAG chat + evidence
│   │   │   ├── MultiChatPage.jsx    # Multi-doc chat (NEW)
│   │   │   ├── SearchPage.jsx       # Semantic search
│   │   │   └── ComparePage.jsx      # Document comparison
│   │   ├── services/api.js      # Axios API client
│   │   ├── App.jsx              # Layout + routing
│   │   └── index.css            # Theme system + animations
│   └── vercel.json              # Vercel deployment config
├── tests/                       # Pytest test suite
└── requirements.txt             # Python dependencies
```

---

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI / OpenRouter API key | — (required) |
| `OPENAI_API_BASE` | LLM API base URL | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | LLM model identifier | `gpt-3.5-turbo` |
| `DATABASE_URL` | Database connection string | `sqlite+aiosqlite:///./data/app.db` |
| `EMBEDDING_MODEL` | SentenceTransformer model | `all-MiniLM-L6-v2` |
| `MAX_FILE_SIZE_MB` | Max upload file size | `50` |
| `REDIS_URL` | Redis URL for Celery | `redis://localhost:6379/0` |
| `CORS_ORIGINS` | Allowed CORS origins | `*` |
| `ENABLE_MULTI_DOC_CHAT` | Toggle multi-doc chat | `true` |
| `ENABLE_REPORT_GENERATION` | Toggle report generation | `true` |
| `ENABLE_HIGHLIGHTS` | Toggle evidence highlights | `true` |

---

## 🧪 Testing

```bash
pip install pytest pytest-asyncio
python -m pytest tests/ -v
```

---

## 🧠 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **`safe_llm_call()` wrapper** | Prevents API hangs — every LLM call has a hard timeout (15–20s) and returns a graceful fallback on failure |
| **Isolated v2 services** | `rag_service_v2.py` and `report_service.py` are completely independent — zero risk to existing RAG pipeline |
| **Feature flags** | Each new feature can be disabled via env vars without code changes or redeployment |
| **Bounded FAISS over-fetch** | Hard cap of 50 prevents O(n) scans on large indices |
| **Token-aware context** | Round-robin document balancing with 6,000-token budget prevents context overflow |
| **Insight caching** | Report generator reuses existing insights from DB — avoids redundant LLM calls |
| **Optional Celery** | Falls back to inline processing when Redis isn't available — works out of the box |

---

## ⚠️ Deployment Note

> This project is designed as a **full-stack AI platform** optimized for **local execution and demonstration**. The architecture is production-ready and can be deployed to any cloud platform (Render, Railway, Fly.io, AWS) by adding the appropriate configuration files and setting environment variables.

---

## 📸 Screenshots

| View | Description |
|------|-------------|
| ![Dashboard](docs/dashboard-with-data.png) | **Dashboard** — Animated stats, charts, document pipeline |
| | **Chat** — RAG conversation with source citations and evidence highlights |
| | **Highlight Navigation** — Click evidence → auto-scroll to highlighted text |
| | **Report** — PDF download with executive summary, risks, extractions |
| | **Multi-Chat** — Cross-document Q&A with grouped sources |

---

## 📄 License

MIT — free for personal and commercial use.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/aditya-3526">Aditya Aryan</a>
</p>
