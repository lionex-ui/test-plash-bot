from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram_i18n import I18nContext

from src.config import bot_config
from src.repositories import UsersRepository
from src.utils import logger

router = Router(name=__name__)


@router.message(Command("add-admin"))
async def handle_add_admin(
    message: types.Message, command: CommandObject, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository
):
    try:
        admin_id = int(command.args)
    except ValueError:
        return

    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] send /add-admin.")
    await state.clear()

    if message.from_user.id == bot_config.main_admin_id:
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to add admins.")

        users_repo.add_admin(admin_id)

        await message.answer(text=i18n.get("admins_list_updated_text"))


@router.message(Command("delete-admin"))
async def handle_delete_admin(
    message: types.Message, command: CommandObject, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository
):
    try:
        admin_id = int(command.args)
    except ValueError:
        return

    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] send /delete-admin.")
    await state.clear()

    if message.from_user.id == bot_config.main_admin_id:
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to delete admins.")

        users_repo.delete_admin(admin_id)

        await message.answer(text=i18n.get("admins_list_updated_text"))
