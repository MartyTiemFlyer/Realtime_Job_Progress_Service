# celery_app.py - Конфигурация Celery для асинхронного выполнения задач
from celery import Celery


# Инициализация Celery
celery_app = Celery(
    "realtime_celery_jobs",
    broker="redis://localhost:6379/0", 
    backend = "redis://localhost:6379/0"     
)

celery_app.autodiscover_tasks(["app.workers"]) # механизм Celery, который сам находит файлы с задачами.

celery_app.conf.update( 
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)

