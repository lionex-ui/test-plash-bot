from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram_i18n import I18nContext
from aiogram_i18n.lazy.filter import LazyFilter

from src.repositories import UsersRepository, TodoRepository
from src.utils import logger

router = Router(name=__name__)


class GetTodoStates(StatesGroup):
    todo_id = State()


@router.message(LazyFilter("get_todo_button"))
@router.message(Command("get-todo"))
async def handle_get_todo_and_request_todo_id(message: types.Message, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] clicked get_todo_button.")
    await state.clear()

    if users_repo.check_bot_access(message.from_user.id):
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to get todo.")
        await message.answer(text=i18n.get("enter_todo_id_text"))

        await state.set_state(GetTodoStates.todo_id)


@router.message(GetTodoStates.todo_id, F.text.isdigit())
async def handle_todo_id_and_get_todo(message: types.Message, state: FSMContext, i18n: I18nContext, todo_repo: TodoRepository):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] entered todo id.")
    await state.clear()

    todo_id = int(message.text)
    if await todo_repo.check_todo_id(message.from_user.id, todo_id):
        todo = await todo_repo.get(todo_id)

        if todo is not None:
            return await message.answer(text=i18n.get("todo_result_text", id=todo.id, description=todo.description))

    await message.answer(text=i18n.get("no_todo_in_list_text"))
