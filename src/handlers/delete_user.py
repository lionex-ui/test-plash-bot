from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram_i18n import I18nContext
from aiogram_i18n.lazy.filter import LazyFilter

from src.keyboards import get_users_keyboard
from src.repositories import UsersRepository
from src.utils import logger

router = Router(name=__name__)


class DeleteUserStates(StatesGroup):
    user_id = State()


@router.message(LazyFilter("delete_user_button"))
@router.message(Command("delete-user"))
async def handle_delete_user_and_show_users_list(
    message: types.Message, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository
):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] clicked delete_user_button.")
    await state.clear()

    if users_repo.check_admin_access(message.from_user.id):
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to delete users.")
        await message.answer(
            text=i18n.get("select_user_text"), reply_markup=get_users_keyboard(users_repo.get_all_users())
        )

        await state.set_state(DeleteUserStates.user_id)


@router.callback_query(DeleteUserStates.user_id, F.data.startswith("user:"))
async def handle_user_select_and_delete_user(
    callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository
):
    logger.info(
        f"User [{callback.from_user.username} | {callback.from_user.id}] selected user [{callback.data.split(':')[1]}]"
    )
    await state.clear()

    users_repo.delete_user(int(callback.data.split(":")[1]))

    await callback.message.edit_text(text=i18n.get("users_list_updated_text"))
