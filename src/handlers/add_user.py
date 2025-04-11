from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram_i18n import I18nContext
from aiogram_i18n.lazy.filter import LazyFilter

from src.repositories import UsersRepository
from src.utils import logger

router = Router(name=__name__)


class AddUserStates(StatesGroup):
    user_id = State()
    group = State()


@router.message(LazyFilter("add_user_button"))
@router.message(Command("add-user"))
async def handle_add_user_and_request_user_id(
    message: types.Message, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository
):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] clicked add_user_button.")
    await state.clear()

    if users_repo.check_admin_access(message.from_user.id):
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to add users.")
        await message.answer(text=i18n.get("enter_user_id_text"))

        await state.set_state(AddUserStates.user_id)


@router.message(AddUserStates.user_id, F.text.isdigit())
async def handle_user_id_and_request_group(message: types.Message, state: FSMContext, i18n: I18nContext):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] entered user_id [{message.text}].")
    await state.update_data(user_id=int(message.text))

    await message.answer(text=i18n.get("enter_group_text"))

    await state.set_state(AddUserStates.group)


@router.message(AddUserStates.group)
async def handle_group_and_add_user(
    message: types.Message, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository
):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] entered group [{message.text}].")

    data = await state.get_data()
    user_id = data["user_id"]
    group = message.text
    await state.clear()

    users_repo.add_or_edit_user(user_id, group)

    await message.answer(text=i18n.get("users_list_updated_text"))
