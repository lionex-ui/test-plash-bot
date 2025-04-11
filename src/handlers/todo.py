from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext
from aiogram_i18n.lazy.filter import LazyFilter

from src.keyboards import get_todo_keyboard
from src.repositories import UsersRepository
from src.utils import logger

router = Router(name=__name__)


@router.message(LazyFilter("todo_button"))
async def handle_todo_button_and_show_todo_buttons(message: types.Message, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] clicked todo_button.")
    await state.clear()

    if users_repo.check_bot_access(message.from_user.id):
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to todo.")
        await message.answer(text=i18n.get("todo_panel_text"), reply_markup=get_todo_keyboard(i18n))
