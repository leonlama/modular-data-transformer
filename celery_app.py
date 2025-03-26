# celery_app.py
import os
import sys
from celery import Celery

# Ensure the parent directory is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Get Redis URL from environment
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

# Create Celery instance with broker URL
celery_app = Celery("modular_data_transformer", broker=redis_url)

# Set result backend to same Redis instance
celery_app.conf.result_backend = redis_url

# Update Celery configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json", 
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,  # results expire after 1 hour
)

# Discover tasks from the entire "app" package
celery_app.autodiscover_tasks(["app"])
