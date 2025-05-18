from celery import Celery
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
celery = Celery(
    "tasks",
    backend="redis://localhost:6379/0",
    broker="redis://localhost:6379/0"
)
celery.autodiscover_tasks(['modules_api'])