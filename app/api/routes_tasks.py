# routes_tasks.py - endpoints for tasks

from fastapi import APIRouter
from ..services.task_service import TaskService
from fastapi import HTTPException

router = APIRouter(prefix="/tasks", tags=["tasks"])

task_service = TaskService()


@router.post("/", status_code=201)
async def post_task(task_data: dict):
    """Create a new task."""
    try:
        task = task_service.create_task(task_data)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{task_id}")
async def read_task(task_id: str):
    task = task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task