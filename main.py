import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from aiogram_i18n import I18nMiddleware
from aiogram_i18n.cores import FluentRuntimeCore

from src.config import bot_config, i18n_config
from src.middlewares import UsersRepoMiddleware, TodoRepoMiddleware
from src.utils import logger
from src.handlers import (
    auth_router,
    panels_router,
    add_user_router,
    delete_user_router,
    edit_user_router,
    check_domains_router,
    main_admin_router,
    todo_router,
    create_todo_router,
    get_todo_router,
    get_all_todo_router,
    update_todo_router,
    delete_todo_router,
)


async def main():
    bot = Bot(token=bot_config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    bot_username = (await bot.get_me()).username

    dp = Dispatcher(storage=MemoryStorage())

    i18n = I18nMiddleware(
        core=FluentRuntimeCore(
            path=i18n_config.locales_path,
            default_locale=i18n_config.default_locale,
        ),
        default_locale=i18n_config.default_locale,
    )
    i18n.setup(dp)

    dp.message.middleware(UsersRepoMiddleware())
    dp.callback_query.middleware(UsersRepoMiddleware())

    dp.message.middleware(TodoRepoMiddleware())
    dp.callback_query.middleware(TodoRepoMiddleware())

    dp.include_routers(
        auth_router,
        panels_router,
        add_user_router,
        delete_user_router,
        edit_user_router,
        check_domains_router,
        main_admin_router,
        todo_router,
        create_todo_router,
        get_todo_router,
        get_all_todo_router,
        update_todo_router,
        delete_todo_router,
    )

    logger.info(f"Bot [{bot_username}] started.")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
