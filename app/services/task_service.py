# task_service.py - Главная бизнес-логика задач
# Компонент, который публикует обновления прогресса

import datetime
import json
from threading import Lock
import uuid
from ..db.models import Task, TaskStatus


lock = Lock()  # для потокобезопасной записи в файл

class TaskService:
    DB_FILE = "free_db.json"

    def save_task(self, task: dict):
        """Сохраняем задачу в (JSON файл) безопасно"""
        with lock:  # блокировка на время чтения/записи
            try:
                with open(self.DB_FILE, "r") as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {}

            # Добавляем новую задачу
            data[task["id"]] = task

            # Перезаписываем файл
            with open(self.DB_FILE, "w") as f:
                json.dump(data, f, indent=2, default=str)  # default=str для datetime


class TaskService:
    def __init__(self):
        """Инициализация сервиса, подключение к БД"""
        pass    
    
    def create_task(self):
        """Логика создания новой задачи"""

        task_id = str(uuid.uuid4())
        task = Task(
            id=task_id,
            status=TaskStatus.PENDING,
            progress=0,
            created_at=datetime.utcnow()
        )
        
        self.save_task(task)

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
    
    