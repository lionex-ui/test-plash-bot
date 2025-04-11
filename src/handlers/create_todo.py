from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram_i18n import I18nContext
from aiogram_i18n.lazy.filter import LazyFilter

from src.repositories import UsersRepository, TodoRepository
from src.utils import logger

router = Router(name=__name__)


class CreateTodoStates(StatesGroup):
    description = State()


@router.message(LazyFilter("create_todo_button"))
@router.message(Command("create-todo"))
async def handle_create_todo_and_request_description(message: types.Message, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] clicked create_todo_button.")
    await state.clear()

    if users_repo.check_bot_access(message.from_user.id):
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to create todo.")
        await message.answer(text=i18n.get("enter_todo_description_text"))

        await state.set_state(CreateTodoStates.description)


@router.message(CreateTodoStates.description, F.text.len() <= 2048)
async def handle_description_and_create_todo(message: types.Message, state: FSMContext, i18n: I18nContext, todo_repo: TodoRepository):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] entered description.")
    await state.clear()

    await todo_repo.create(message.from_user.id, message.text)

    await message.answer(text=i18n.get("todo_list_updated_text"))
