from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.database import AsyncSessionLocal
from src.repositories import TodoRepository


class TodoRepoMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        async with AsyncSessionLocal() as session:
            data["todo_repo"] = TodoRepository(session)
            return await handler(event, data)
