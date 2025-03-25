# celery_app.py
import os
from celery import Celery

# Set the Redis URL; adjust if necessary
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("modular_data_transformer", broker=redis_url, backend=redis_url)

# Optional: Configure Celery settings here
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

# Add autodiscovery for tasks in the "app.tasks" module
celery_app.autodiscover_tasks(['app.tasks'])
