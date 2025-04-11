from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram_i18n import I18nContext
from aiogram_i18n.lazy.filter import LazyFilter

from src.keyboards import get_group_edit_choices_keyboard, get_users_keyboard
from src.repositories import UsersRepository
from src.utils import logger

router = Router(name=__name__)


class EditUserStates(StatesGroup):
    user_id = State()
    group_choice = State()
    group = State()


@router.message(LazyFilter("edit_user_button"))
@router.message(Command("edit-user"))
async def handle_edit_user_and_show_users_list(
    message: types.Message, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository
):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] clicked edit_user_button.")
    await state.clear()

    if users_repo.check_admin_access(message.from_user.id):
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to edit users.")
        await message.answer(
            text=i18n.get("select_user_text"), reply_markup=get_users_keyboard(users_repo.get_all_users())
        )

        await state.set_state(EditUserStates.user_id)


@router.callback_query(EditUserStates.user_id, F.data.startswith("user:"))
async def handle_user_select_and_show_group_choices(
    callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext
):
    logger.info(
        f"User [{callback.from_user.username} | {callback.from_user.id}] selected user [{callback.data.split(':')[1]}]"
    )
    await state.update_data(user_id=int(callback.data.split(":")[1]))

    await callback.message.edit_text(
        text=i18n.get("select_group_choice_text"), reply_markup=get_group_edit_choices_keyboard(i18n)
    )

    await state.set_state(EditUserStates.group_choice)


@router.callback_query(EditUserStates.group_choice, F.data == "delete-group")
async def handle_delete_group_and_delete_group_from_user(
    callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository
):
    logger.info(f"User [{callback.from_user.username} | {callback.from_user.id}] selected delete group.")

    data = await state.get_data()
    user_id = data["user_id"]
    group = ""
    await state.clear()

    users_repo.add_or_edit_user(user_id, group)

    await callback.message.edit_text(text=i18n.get("users_list_updated_text"))


@router.callback_query(EditUserStates.group_choice, F.data == "add-group")
async def handle_add_group_and_request_group(callback: types.CallbackQuery, state: FSMContext, i18n: I18nContext):
    logger.info(f"User [{callback.from_user.username} | {callback.from_user.id}] selected add group.")

    await callback.message.edit_text(text=i18n.get("enter_group_text"))

    await state.set_state(EditUserStates.group)


@router.message(EditUserStates.group)
async def handle_group_and_add_group_to_user(
    message: types.Message, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository
):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] entered group [{message.text}].")

    data = await state.get_data()
    user_id = data["user_id"]
    group = message.text
    await state.clear()

    users_repo.add_or_edit_user(user_id, group)

    await message.answer(text=i18n.get("users_list_updated_text"))
