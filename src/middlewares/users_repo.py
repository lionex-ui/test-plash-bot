from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from src.repositories import UsersRepository


class UsersRepoMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data: dict):
        data["users_repo"] = UsersRepository()
        return await handler(event, data)
