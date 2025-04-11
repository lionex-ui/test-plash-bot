import asyncio

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram_i18n import I18nContext
from aiogram_i18n.lazy.filter import LazyFilter

from src.repositories import UsersRepository
from src.utils import check_domain, logger

router = Router(name=__name__)


class CheckDomainsStates(StatesGroup):
    domains = State()


@router.message(LazyFilter("check_domains_button"))
@router.message(Command("search"))
async def handle_check_domains_and_request_domains(
    message: types.Message, state: FSMContext, i18n: I18nContext, users_repo: UsersRepository
):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] clicked check_domains_button.")
    await state.clear()

    if users_repo.check_bot_access(message.from_user.id):
        logger.info(f"User [{message.from_user.username} | {message.from_user.id}] has access to check domains.")
        await message.answer(text=i18n.get("enter_domains_text"))

        await state.set_state(CheckDomainsStates.domains)


@router.message(CheckDomainsStates.domains)
async def handle_domains_and_check_domains(message: types.Message, state: FSMContext, i18n: I18nContext):
    logger.info(f"User [{message.from_user.username} | {message.from_user.id}] entered domains.")
    await state.clear()

    domains = message.text.split("\n")
    tasks = [check_domain(domain, i18n) for domain in domains]
    results = await asyncio.gather(*tasks)

    for result in results:
        await message.answer(text=i18n.get("domain_result_text", **result), disable_web_page_preview=True)
