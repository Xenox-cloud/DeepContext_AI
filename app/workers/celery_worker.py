"""
Celery Worker Configuration

Configures Celery worker for async task processing.
"""

from celery import Celery
from app.core.config import settings


# Create Celery app
celery_app = Celery(
    "enterprise_nlp_platform",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)
# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    task_soft_time_limit=300,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)
