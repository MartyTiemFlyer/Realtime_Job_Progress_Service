# websocket_manager.py - Менеджер WebSocket соединений
# websocat ws://localhost:8000/ws/tasks/1
import asyncio
from fastapi import WebSocket
import redis.asyncio as redis
redis_client = redis.Redis()


class WebSocketManager:
    def __init__(self):
        """Инициализация менеджера """
        self.connections: dict[str, list[WebSocket]] = {}
        self.listeners: dict[str, asyncio.Task] = {}
    
    
    async def send_to_task(self, task_id: str, message: str) -> None:
        """
        Отправляет текстовое сообщение всем активным соединениям.
        """
        if task_id in self.connections:
            connections = self.connections.get(task_id)
            # используем copy() для безопасной итерации при возможных изменениях списка
            for connection in connections.copy(): 
                try:
                    await connection.send_text(message)
                except Exception as e:
                    print(f"Error occurred while sending message to connection: {e}")
                    self.disconnect(task_id, connection)
                    
                    
    async def _listen_to_task_updates(self, task_id: str):
        """
        Метод для прослушивания обновлений о задаче.
        """
        print(f"Listener started for task_id = {task_id}")
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(f"task:{task_id}")
        try:
            while True:
                message = await pubsub.get_message(ignore_subscribe_messages=True)
                if message and message["type"] == "message":
                    data = message["data"]
                    await self.send_to_task(task_id, data.decode("utf-8"))
                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            print(f"Listener stopped for {task_id}")
            await pubsub.unsubscribe(f"task:{task_id}")
            await pubsub.close()
                
    async def connect(self, task_id: str, websocket: WebSocket) -> None:
        """
        Принимает новое WebSocket соединение и добавляет его в список активных.
        Слушатель для обновлений по задаче запускается при первом подключении к данной задаче.
        """
        if task_id not in self.connections:
            self.connections[task_id] = []

        self.connections[task_id].append(websocket)
        
        # Если для данной задачи еще нет слушателя, запускаем его   
        if task_id not in self.listeners:
            # Запускаем фоновую задачу для прослушивания обновлений
            self.listeners[task_id] = asyncio.create_task(self._listen_to_task_updates(task_id))
        

    async def disconnect(self, task_id: str, websocket: WebSocket) -> None:
        """
        Удаляет WebSocket соединение из словаря активных.
        """
        if task_id in self.connections:
            connections = self.connections.get(task_id)
            if websocket in connections:
                connections.remove(websocket)
                if not connections:  
                    del self.connections[task_id]

        # Если для данной задачи больше нет активных соединений, отменяем слушателя
        if task_id in self.listeners and task_id not in self.connections:
            listener_task = self.listeners.pop(task_id)
            listener_task.cancel()
            try:
                await listener_task
            except asyncio.CancelledError:
                pass
            
        