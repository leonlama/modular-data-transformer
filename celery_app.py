# celery_app.py
import os
import sys
from celery import Celery

# Insert the parent directory if needed
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Get Redis URL from environment
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("modular_data_transformer", broker=redis_url, backend=redis_url)

celery_app.conf.update(
    broker_url=redis_url,
    result_backend=redis_url,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,
)

# This is enough to discover tasks in "app.tasks"
celery_app.autodiscover_tasks(['app'])
