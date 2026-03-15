# websocket_manager.py - Менеджер WebSocket соединений

from fastapi import WebSocket


class WebSocketManager:
    def __init__(self):
        """Инициализация менеджера с пустым словарем"""
        self.connections: dict[str, list[WebSocket]] = {}

    async def connect(self, task_id: str, websocket: WebSocket) -> None:
        """
        Принимает новое WebSocket соединение и добавляет его в список активных.
        """
        if task_id not in self.connections:
            self.connections[task_id] = []

        self.connections[task_id].append(websocket)

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
                

