from .settings import Settings


class DBConfig(Settings):
    database_url: str = "driver://user:pass@ip:port/dbname"


db_config = DBConfig()
