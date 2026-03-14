from fastapi import FastAPI, WebSocket
from app.api.routes_tasks import router as tasks_router

app = FastAPI()

app.include_router(tasks_router)
# Команда запуска:
# uvicorn main:app --reload


@app.websocket("/ws/tasks/{task_id}")
async def task_ws(websocket: WebSocket, task_id: str):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Task {task_id}: {data}")