# models.py - Определение моделей данных для задач и прогресса
from sqlalchemy import Column, Enum, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from datetime import datetime
#Base = declarative_base()


class TaskStatus(str, Enum):
    PENDING = "pending"     # задача создана, но worker ещё не начал
    STARTED = "started"     # worker начал выполнение задачи
    PROGRESS = "progress"   # задача в процессе выполнения
    SUCCESS = "success"     # задача выполнена успешно
    FAILED = "failed"       # задача завершена с ошибкой


class Task(BaseModel):
    id: str
    status: str
    progress: int = 0   # процент выполнения
    created_at: datetime
    

