"""
FastAPI Application Main Module

Initializes and configures the FastAPI application with all routers,
middleware, and dependencies.
"""
from app.db.base import Base
from app.db.session import engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import upload, search, classify, health, rag
from app.core.config import settings
from app.core.logging import setup_logging
from contextlib import asynccontextmanager
from app.services.embedding_service import EmbeddingService
from app.api.routes import upload, search, classify, health, documents

# Setup logging
setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.embedding_service = EmbeddingService()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise NLP Platform - Production-grade backend-first NLP platform",
    docs_url=f"{settings.api_v1_prefix}/docs",
    redoc_url=f"{settings.api_v1_prefix}/redoc",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(health.router, prefix=settings.api_v1_prefix, tags=["health"])
app.include_router(upload.router, prefix=settings.api_v1_prefix, tags=["upload"])
app.include_router(search.router, prefix=settings.api_v1_prefix, tags=["search"])
app.include_router(classify.router, prefix=settings.api_v1_prefix, tags=["classify"])
app.include_router(documents.router, prefix=settings.api_v1_prefix, tags=["documents"])
app.include_router(rag.router, prefix=settings.api_v1_prefix, tags=["rag"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
