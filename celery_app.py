# celery_app.py
import os
import sys
from celery import Celery

# Set project root as the directory of celery_app.py so that "app" is importable
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Create Celery instance
celery_app = Celery("modular_data_transformer")

# Get Redis URL from environment and configure broker/backend
redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
celery_app.conf.broker_url = redis_url
celery_app.conf.result_backend = redis_url
celery_app.conf.task_ignore_result = False

# Enable connection retries on startup
celery_app.conf.broker_connection_retry_on_startup = True
celery_app.conf.broker_transport_options = {
    'max_retries': 3,       # number of retry attempts
    'interval_start': 0,    # initial retry delay in seconds
    'interval_step': 0.2,   # incremental increase for subsequent retries
    'interval_max': 0.5,    # maximum retry delay in seconds
}

# Update Celery configuration
celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    result_expires=3600,  # results expire after 1 hour
)

# Force import of tasks so they are registered
import app.tasks

# IMPORTANT: Autodiscover tasks from the 'app' package
celery_app.autodiscover_tasks(["app"])
