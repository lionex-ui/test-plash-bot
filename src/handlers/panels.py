from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from aiogram_i18n.lazy.filter import LazyFilter

from src.keyboards import get_admin_panel_keyboard, get_user_keyboard
from src.repositories import UsersRepository
from src.utils import logger

router = Router(name=__name__)


@router.message(LazyFilter("admin_panel_button"))
async def handle_admin_panel_and_show_admin_buttons(
    message: types.Message, i18n: I18nContext, state: FSMContext, users_repo: UsersRepository
):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] clicked admin_panel_button.")
    await state.clear()

    if users_repo.check_admin_access(message.from_user.id):
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to admin panel.")
        await message.answer(text=i18n.get("admin_panel_text"), reply_markup=get_admin_panel_keyboard(i18n))


@router.message(LazyFilter("user_panel_button"))
async def handle_user_panel_and_show_user_buttons(
    message: types.Message, i18n: I18nContext, state: FSMContext, users_repo: UsersRepository
):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] clicked user_panel_button.")
    await state.clear()

    if users_repo.check_admin_access(message.from_user.id):
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to user panel.")
        await message.answer(text=i18n.get("user_panel_text"), reply_markup=get_user_keyboard(i18n))
