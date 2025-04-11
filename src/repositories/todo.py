from sqlalchemy import select, update, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import TodoModel


class TodoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_todo_id(self, user_id: int, todo_id: int) -> bool:
        result = await self.session.execute(
            select(TodoModel)
            .filter(and_(TodoModel.telegram_id == user_id, TodoModel.id == todo_id))
        )

        return result.scalar() is not None

    async def get_all(self, user_id: int) -> list[TodoModel]:
        result = await self.session.execute(select(TodoModel).filter(TodoModel.telegram_id == user_id))
        todo_list = result.scalars().all()

        return list(todo_list)

    async def get(self, todo_id: int) -> TodoModel | None:
        result = await self.session.execute(select(TodoModel).filter(TodoModel.id == todo_id))

        return result.scalar()

    async def create(self, user_id: int, description: str) -> None:
        self.session.add(TodoModel(telegram_id=user_id, description=description))
        await self.session.commit()

    async def update(self, todo_id: int, description: str) -> None:
        await self.session.execute(update(TodoModel).values(description=description).filter(TodoModel.id == todo_id))
        await self.session.commit()

    async def delete(self, todo_id: int) -> None:
        await self.session.execute(delete(TodoModel).filter(TodoModel.id == todo_id))
        await self.session.commit()
