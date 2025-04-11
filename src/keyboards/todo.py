from aiogram import types
from aiogram_i18n import I18nContext


def get_todo_keyboard(i18n: I18nContext) -> types.ReplyKeyboardMarkup:
    return types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=i18n.get("create_todo_button"))],
            [types.KeyboardButton(text=i18n.get("get_todo_button"))],
            [types.KeyboardButton(text=i18n.get("get_all_todo_button"))],
            [types.KeyboardButton(text=i18n.get("edit_todo_button"))],
            [types.KeyboardButton(text=i18n.get("delete_todo_button"))],
            [types.KeyboardButton(text=i18n.get("back_button"))],
        ]
    )
