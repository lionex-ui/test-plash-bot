from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from aiogram_i18n.lazy.filter import LazyFilter

from src.keyboards import get_auth_keyboard
from src.repositories import UsersRepository
from src.utils import logger

router = Router(name=__name__)


@router.message(CommandStart())
@router.message(LazyFilter("back_button"))
async def handle_start_or_back_and_check_access(
    message: types.Message, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository
):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] sent /start.")
    await state.clear()

    if users_repo.check_bot_access(message.from_user.id):
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access.")
        await message.answer(
            text=i18n.get("welcome_text"),
            reply_markup=get_auth_keyboard(users_repo.check_admin_access(message.from_user.id), i18n),
        )
