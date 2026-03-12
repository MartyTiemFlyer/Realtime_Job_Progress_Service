# tasks.py - Асинхронные задачи для Celery
from .celery_app import celery_app
import redis, json

# глобальный Redis клиент для воркера
redis_client = redis.Redis(host="localhost", port=6379, db=0)


def publish_event(task_id, status, progress=0, message=""):
    """Функция для публикации прогресса задачи"""
    print(f"Task {task_id} progress: {progress}%")
    
    
    event = {
        "task_id": task_id,
        "status": status,
        "progress": progress,
        "message": message
    }
    redis_client.publish("task_progress", json.dumps(event))
    print(f"Published event: {event}")


@celery_app.task
def process_task(task_id):
    """Пример задачи, которая выполняется асинхронно
    после каждого шага publish
    """
    publish_event(task_id, status="started", progress=0)

    import time
    for i in range(1, 5):
        time.sleep(1)  # имитация работы
        progress = i * 3
        publish_event(task_id, status="progress", progress=progress)

    publish_event(task_id, status="finished", progress=100)
    print(f"Task {task_id} completed.")
    
    

