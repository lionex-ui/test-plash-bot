from aiogram import types
from aiogram_i18n import I18nContext


def get_auth_keyboard(is_admin: bool, i18n: I18nContext) -> types.ReplyKeyboardMarkup:
    if is_admin:
        return get_admin_keyboard(i18n)
    else:
        return get_user_keyboard(i18n)


def get_admin_keyboard(i18n: I18nContext) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=i18n.get("admin_panel_button"))],
            [types.KeyboardButton(text=i18n.get("user_panel_button"))],
        ],
        resize_keyboard=True,
    )


def get_user_keyboard(i18n: I18nContext) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=i18n.get("check_domains_button"))],
            [types.KeyboardButton(text=i18n.get("todo_button"))],
            [types.KeyboardButton(text=i18n.get("back_button"))],
        ],
        resize_keyboard=True,
    )
