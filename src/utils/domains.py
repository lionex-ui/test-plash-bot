import httpx
from aiogram_i18n import I18nContext

from .log import logger


async def check_domain(domain: str, i18n: I18nContext) -> dict:
    if not domain.startswith("http://") and not domain.startswith("https://"):
        domain = "https://" + domain

    async with httpx.AsyncClient(http2=True) as client:
        try:
            resp = await client.get(domain)

            result = {
                "domain": domain,
                "ssl": "OK" if domain.startswith("https://") else "NOT OK",
                "status": resp.status_code,
                "availability": i18n.get("domain_available_text"),
            }
        except Exception as e:
            logger.error(f"Error in request: {e}")

            result = {
                "domain": domain,
                "ssl": "OK" if domain.startswith("https://") and "SSL" not in str(e) else "NOT OK",
                "status": 500,
                "availability": i18n.get("domain_not_available_text"),
            }

    return result
