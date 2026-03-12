# task_service.py - Главная бизнес-логика задач
# Компонент, который публикует обновления прогресса

import datetime
import json
from threading import Lock
import uuid

from app.workers.tasks import process_task
from ..db.models import Task, TaskStatus


lock = Lock()  # для потокобезопасной записи в файл

class TaskService:
    DB_FILE = "app/db/free_db.json"
    def __init__(self):
        """Инициализация сервиса, подключение к БД"""
        pass 

    def save_task(self, task):
        """Сохраняем задачу в (JSON файл) безопасно"""
        with lock:  # блокировка на время чтения/записи
            try:
                with open(self.DB_FILE, "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {}

            # Добавляем новую задачу
            task_dict = task.__dict__ if hasattr(task, '__dict__') else task
            data[task_dict["id"]] = task_dict

            # Перезаписываем файл
            with open(self.DB_FILE, "w") as f:
                json.dump(data, f, indent=2, default=str)  # default=str для datetime

    
    def create_task(self, task_data: dict):
        """Логика создания новой задачи"""

        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            status=TaskStatus.PENDING,
            progress=0,
            created_at=datetime.datetime.utcnow()
        )
        
        self.save_task(task)
        result = process_task.delay(task_id) # запускаем асинхронную задачу в Celery

        return task
    
    def get_task(self, task_id: str):
        """Получение задачи по ID"""
        with lock:
            try:
                with open(self.DB_FILE, "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                return None

            task_data = data.get(task_id)
            if not task_data:
                return None
            
            # Преобразуем словарь обратно в объект Task
            task = Task(**task_data)
            return task
    
    def update_task(self, task_id: str, status: TaskStatus | None = None, progress: int | None = None):
        """Обновление статуса и прогресса задачи"""
        with lock:
            try:
                with open(self.DB_FILE, "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                return None

            task_data = data.get(task_id)
            if not task_data:
                return None
            
            if status is not None:
                task_data["status"] = status
            if progress is not None:
                task_data["progress"] = progress
            
            # Сохраняем обновленную задачу
            data[task_id] = task_data
            with open(self.DB_FILE, "w") as f:
                json.dump(data, f, indent=2, default=str)

            return Task(**task_data)
    