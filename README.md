# Enterprise NLP Platform

A production-grade, backend-first NLP platform built with FastAPI, SQLAlchemy, PostgreSQL, Qdrant, Redis, and Celery.

## Features

- Document Upload and Processing
- Intelligent Chunking
- Semantic Search with Qdrant
- Document Classification
- Reranking Capabilities
- Async-Ready Architecture
- Production-Grade Logging
- Type-Hinted Codebase

## Architecture

```
enterprise_nlp_platform/
├── app/
│   ├── api/          # FastAPI routes and dependencies
│   ├── core/         # Configuration, security, logging
│   ├── db/           # Database models and sessions
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic services
│   ├── workers/      # Celery workers and tasks
│   └── utils/        # Utilities (chunking, file loading)
├── uploads/          # Uploaded files
├── tests/            # Test suite
└── requirements.txt  # Dependencies
```

## Prerequisites

- Python 3.12+
- PostgreSQL
- Redis
- Qdrant

## Quick Start

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows**:
```bash
venv\Scripts\activate
```

**Linux/Mac**:
```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Copy `.env.example` to `.env` and update with your configuration:

```bash
copy .env.example .env
```

### Run FastAPI Application

```bash
python run.py
```

### Run Celery Worker

```bash
celery -A app.workers.celery_worker worker --loglevel=info
```

## API Endpoints

- `POST /api/v1/upload` - Upload documents
- `POST /api/v1/search` - Semantic search
- `POST /api/v1/classify` - Classify documents
- `GET /api/v1/health` - Health check

## Development

The platform follows clean architecture principles with:
- Modular structure
- Type hints throughout
- Async-first design
- Environment-based configuration
- Production-grade logging

## License

Enterprise NLP Platform
