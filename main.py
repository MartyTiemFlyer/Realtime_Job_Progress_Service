from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.api.routes_tasks import router as tasks_router
from app.services.websocket_manager import WebSocketManager

app = FastAPI()
manager = WebSocketManager()
app.include_router(tasks_router)
# Команда запуска:
# uvicorn main:app --reload


@app.websocket("/ws/tasks/{task_id}")
async def task_ws(websocket: WebSocket, task_id: str):
    await websocket.accept()
    await manager.connect(task_id, websocket)
    print(manager.connections)
    try: 
        while True:
            client_message = await websocket.receive_text()
    except WebSocketDisconnect as socketDisconnect:
        print(f"WebSocket disconnected: {socketDisconnect}")
    finally:
        await manager.disconnect(task_id, websocket)
           
        