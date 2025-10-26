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
        ban_users_ids = []
        for user in cursor:
            if 'user_id' not in user:
                continue
            uid = user['user_id']
            if isinstance(uid, dict) and '$numberLong' in uid:
                ban_users_ids.append(int(uid['$numberLong']))
            else:
                ban_users_ids.append(int(uid))
        return ban_users_ids

    async def get_users(self) -> List[int]:
        cursor = self.users.find({})
        users_ids = []
        for user in cursor:
            if 'user_id' not in user:
                continue
            uid = user['user_id']
            if isinstance(uid, dict) and '$numberLong' in uid:
                users_ids.append(int(uid['$numberLong']))
            else:
                users_ids.append(int(uid))
        return users_ids

    async def get_admins(self) -> List[int]:
        cursor = self.admins.find({})
        admin_ids = []
        for admin in cursor:
            if 'user_id' not in admin:
                continue
            uid = admin['user_id']
            if isinstance(uid, dict) and '$numberLong' in uid:
                admin_ids.append(int(uid['$numberLong']))
            else:
                admin_ids.append(int(uid))
        return admin_ids


db = DB()
