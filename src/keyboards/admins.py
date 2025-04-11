from aiogram import types
from aiogram_i18n import I18nContext


def get_admin_panel_keyboard(i18n: I18nContext) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=i18n.get("add_user_button"))],
            [types.KeyboardButton(text=i18n.get("delete_user_button"))],
            [types.KeyboardButton(text=i18n.get("edit_user_button"))],
            [types.KeyboardButton(text=i18n.get("back_button"))],
        ]
    )


def get_users_keyboard(users: list[dict]) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=str(user["telegram_id"]), callback_data=f"user:{user['telegram_id']}")]
            for user in users
        ]
    )


def get_group_edit_choices_keyboard(i18n: I18nContext) -> types.InlineKeyboardMarkup:
    return types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text=i18n.get("delete_group_button"), callback_data="delete-group")],
            [types.InlineKeyboardButton(text=i18n.get("add_group_button"), callback_data="add-group")],
        ]
    )
