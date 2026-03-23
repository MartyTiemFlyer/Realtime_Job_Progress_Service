from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes_tasks import router as tasks_router
from app.services.websocket_manager import WebSocketManager

app = FastAPI()
manager = WebSocketManager()
app.include_router(tasks_router)
# Команда запуска:
# uvicorn main:app --reload

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"])

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
    
app.mount("/client", StaticFiles(directory="client"), name="client")
          
          
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("client/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
