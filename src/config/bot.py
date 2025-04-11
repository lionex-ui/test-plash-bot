from .settings import Settings


class BotConfig(Settings):
    bot_token: str = "token"
    main_admin_id: int = 0


bot_config = BotConfig()
