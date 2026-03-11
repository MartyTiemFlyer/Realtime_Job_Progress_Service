# celery_app.py - Конфигурация Celery для асинхронного выполнения задач
from celery import Celery
from app.workers import tasks


# Инициализация Celery
celery_app = Celery(
    "realtime_celery_jobs",
    broker="redis://localhost:6379/0", 
    backend = "redis://localhost:6379/0"
    
      
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json']
)


@celery_app.task
def process_task(task_id):
    """Пример задачи, которая выполняется асинхронно"""
    print(f"Processing task {task_id}...")
    # Здесь можно добавить логику обработки задачи, например, имитацию долгой работы
    import time
    time.sleep(4)  # имитация долгой работы
    print(f"Task {task_id} completed.")