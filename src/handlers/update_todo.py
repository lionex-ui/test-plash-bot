from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram_i18n import I18nContext
from aiogram_i18n.lazy.filter import LazyFilter

from src.repositories import TodoRepository, UsersRepository
from src.utils import logger

router = Router(name=__name__)


class UpdateTodoStates(StatesGroup):
    todo_id = State()
    description = State()


@router.message(LazyFilter("edit_todo_button"))
@router.message(Command("update-todo"))
async def handle_update_todo_and_request_todo_id(
    message: types.Message, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository
):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] clicked edit_todo_button.")
    await state.clear()

    if users_repo.check_bot_access(message.from_user.id):
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to update todo.")
        await message.answer(text=i18n.get("enter_todo_id_text"))

        await state.set_state(UpdateTodoStates.todo_id)


@router.message(UpdateTodoStates.todo_id, F.text.isdigit())
async def handle_todo_id_and_request_description(
    message: types.Message, state: FSMContext, i18n: I18nContext, todo_repo: TodoRepository
):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] entered todo id.")

    if not await todo_repo.check_todo_id(message.from_user.id, int(message.text)):
        await message.answer(text=i18n.get("no_todo_in_list_text"))
        await state.clear()
        return

    await state.update_data(todo_id=int(message.text))
    await message.answer(text=i18n.get("enter_todo_description_text"))

    await state.set_state(UpdateTodoStates.description)


@router.message(UpdateTodoStates.description, F.text.len() <= 2048)
async def handle_description_and_update_todo(
    message: types.Message, state: FSMContext, i18n: I18nContext, todo_repo: TodoRepository
):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] entered description.")

    data = await state.get_data()
    todo_id = data["todo_id"]
    description = message.text
    await state.clear()

    await todo_repo.update(todo_id, description)

    await message.answer(text=i18n.get("todo_list_updated_text"))
