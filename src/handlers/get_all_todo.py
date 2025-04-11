from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from aiogram_i18n.lazy.filter import LazyFilter

from src.repositories import UsersRepository, TodoRepository
from src.utils import logger

router = Router(name=__name__)


@router.message(LazyFilter("get_all_todo_button"))
@router.message(Command("get-all_todo"))
async def handle_get_all_todo_and_show_todo_list(message: types.Message, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository, todo_repo: TodoRepository):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] clicked get_all_todo_button.")
    await state.clear()

    if users_repo.check_bot_access(message.from_user.id):
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to get all todo.")

        todo_list = await todo_repo.get_all(message.from_user.id)
        if len(todo_list) == 0:
            return await message.answer(text=i18n.get("no_todo_text"))

        for todo in todo_list:
            await message.answer(i18n.get("todo_result_text", id=todo.id, description=todo.description))
