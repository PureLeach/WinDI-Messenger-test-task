from uuid import UUID

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: dict[UUID, dict[UUID, WebSocket]] = {}

    async def connect(self, chat_id: UUID, user_id: UUID, websocket: WebSocket) -> None:
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = {}
        self.active_connections[chat_id][user_id] = websocket

    def disconnect(self, chat_id: UUID, user_id: UUID) -> None:
        self.active_connections.get(chat_id, {}).pop(user_id, None)

    async def send_personal_message(self, message: dict, chat_id: UUID, user_id: UUID) -> None:
        if ws := self.active_connections.get(chat_id, {}).get(user_id):
            await ws.send_json(message)

    async def broadcast_to_chat(self, chat_id: UUID, message: dict) -> None:
        for user_id in self.active_connections.get(chat_id, {}):
            await self.send_personal_message(message, chat_id, user_id)


manager = ConnectionManager()
