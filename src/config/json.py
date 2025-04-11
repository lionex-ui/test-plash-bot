import os

from .settings import Settings


class JSONConfig(Settings):
    json_path: str = os.path.join(os.getcwd(), "src", "files", "users.json")


json_config = JSONConfig()
