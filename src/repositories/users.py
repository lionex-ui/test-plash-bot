import json

from src.config import json_config


class UsersRepository:
    def __init__(self):
        self.__users, self.__admins = self.__read_json()

    # noinspection PyMethodMayBeStatic
    def __read_json(self) -> tuple[dict, set]:
        with open(json_config.json_path, encoding="utf-8") as json_file:
            content = json.load(json_file)

        return {user["telegram_id"]: user for user in content["users"]}, set(content["admins"])

    def __write_json(self) -> None:
        users = list(self.__users.values())
        admins = list(self.__admins)

        with open(json_config.json_path, "w", encoding="utf-8") as json_file:
            json.dump({"users": users, "admins": admins}, json_file, indent=4, ensure_ascii=False)  # type: ignore

    def check_bot_access(self, user_id: int) -> bool:
        return user_id in self.__users or user_id in self.__admins

    def check_admin_access(self, user_id: int) -> bool:
        return user_id in self.__admins

    def add_admin(self, user_id: int) -> None:
        self.__admins.add(user_id)
        self.__write_json()

    def delete_admin(self, user_id: int) -> None:
        self.__admins.remove(user_id)
        self.__write_json()

    def get_user(self, user_id: int) -> dict | None:
        return self.__users.get(user_id)

    def get_all_users(self) -> list:
        return list(self.__users.values())

    def add_or_edit_user(self, user_id: int, group: str) -> None:
        self.__users[user_id] = {"telegram_id": user_id, "group": group}
        self.__write_json()

    def delete_user(self, user_id: int) -> None:
        del self.__users[user_id]
        self.__write_json()
