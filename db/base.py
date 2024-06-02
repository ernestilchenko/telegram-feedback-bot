import logging
from typing import List

from pymongo import errors
from pymongo.mongo_client import MongoClient

from bot.config import MONGO_URL


class DB:

    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client["helper_bot"]
        self.users = self.db["users"]
        self.admins = self.db["admin"]
        self.ban = self.db["ban"]
        self.users.create_index("user_id", unique=True)
        self.admins.create_index("user_id", unique=True)

    async def add_user(self, user_id: int) -> None:
        data = {
            "user_id": user_id,
        }
        try:
            self.users.insert_one(data)
        except errors.DuplicateKeyError:
            logging.info(f"User {user_id} already exists")

    async def add_admin(self, user_id: int) -> None:
        data = {
            "user_id": user_id
        }
        try:
            self.admins.insert_one(data)
        except errors.DuplicateKeyError:
            logging.info(f"Admin {user_id} already exists.")

    async def bun_user(self, user_id: int) -> None:
        self.users.delete_one({"user_id": user_id})
        self.ban.insert_one({"user_id": user_id})
        logging.info(f"User {user_id} was banned.")

    async def unban_user(self, user_id: int) -> None:
        self.ban.delete_one({"user_id": user_id})
        self.users.insert_one({"user_id": user_id})
        logging.info(f"User {user_id} was unbanned.")

    async def is_banned(self, user_id: int) -> bool:
        return bool(self.ban.find_one({"user_id": user_id}))

    async def get_ban_users(self) -> List[int]:
        cursor = self.ban.find({})
        ban_users_ids = [user['user_id'] for user in cursor]
        return ban_users_ids

    async def get_users(self) -> List[int]:
        cursor = self.users.find({})
        users_ids = [user['user_id'] for user in cursor]
        return users_ids

    async def get_admins(self) -> List[int]:
        cursor = self.admins.find({})
        admin_ids = [admin['user_id'] for admin in cursor]
        return admin_ids


db = DB()
