# Only if you need to expose the celery_app globally (for Django, etc.)
from .celery_app import celery_app
__all__ = ("celery_app",)
