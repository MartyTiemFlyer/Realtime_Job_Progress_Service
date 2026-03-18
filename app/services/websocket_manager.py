# websocket_manager.py - Менеджер WebSocket соединений

import asyncio

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        """Инициализация менеджера """
        self.connections: dict[str, list[WebSocket]] = {}
        self.listeners: dict[str, asyncio.Task] = {}
        
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
        

    def disconnect(self, task_id: str, websocket: WebSocket) -> None:
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
    
    async def listen_to_task(self, task_id: str):
        """
        Метод для прослушивания обновлений о задаче.
        """
        
        if not self.listeners.get(task_id):
            # Запускаем фоновую задачу для прослушивания обновлений
            self.listeners[task_id] = asyncio.create_task(self._listen_to_task_updates(task_id))
        