from .settings import Settings


class I18nConfig(Settings):
    locales_path: str = "src/locales/{locale}/LC_MESSAGES"
    default_locale: str = "ru"


i18n_config = I18nConfig()
