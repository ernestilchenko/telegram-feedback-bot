import logging
from typing import List

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import errors

from bot.config import MONGO_URL

logger = logging.getLogger(__name__)


class DB:

    def __init__(self):
        self.client = AsyncIOMotorClient(MONGO_URL)
        self.db = self.client["helper_bot"]
        self.users = self.db["users"]
        self.admins = self.db["admin"]
        self.ban = self.db["ban"]

    async def create_indexes(self):
        await self.users.create_index("user_id", unique=True)
        await self.admins.create_index("user_id", unique=True)
        logger.info("Database indexes created")

    async def add_user(self, user_id: int) -> None:
        data = {
            "user_id": user_id,
        }
        try:
            await self.users.insert_one(data)
            logger.info(f"User {user_id} added")
        except errors.DuplicateKeyError:
            logger.debug(f"User {user_id} already exists")

    async def add_admin(self, user_id: int) -> None:
        data = {
            "user_id": user_id
        }
        try:
            await self.admins.insert_one(data)
            logger.info(f"Admin {user_id} added")
        except errors.DuplicateKeyError:
            logger.debug(f"Admin {user_id} already exists")

    async def ban_user(self, user_id: int) -> None:
        await self.users.delete_one({"user_id": user_id})
        await self.ban.insert_one({"user_id": user_id})
        logger.warning(f"User {user_id} was banned")

    async def unban_user(self, user_id: int) -> None:
        await self.ban.delete_one({"user_id": user_id})
        await self.users.insert_one({"user_id": user_id})
        logger.info(f"User {user_id} was unbanned")

    async def is_banned(self, user_id: int) -> bool:
        result = await self.ban.find_one({"user_id": user_id})
        return bool(result)

    async def get_ban_users(self) -> List[int]:
        cursor = self.ban.find({})
        ban_users_ids = []
        async for user in cursor:
            if 'user_id' not in user:
                continue
            uid = user['user_id']
            if isinstance(uid, dict) and '$numberLong' in uid:
                ban_users_ids.append(int(uid['$numberLong']))
            else:
                ban_users_ids.append(int(uid))
        logger.debug(f"Retrieved {len(ban_users_ids)} banned users")
        return ban_users_ids

    async def get_users(self) -> List[int]:
        cursor = self.users.find({})
        users_ids = []
        async for user in cursor:
            if 'user_id' not in user:
                continue
            uid = user['user_id']
            if isinstance(uid, dict) and '$numberLong' in uid:
                users_ids.append(int(uid['$numberLong']))
            else:
                users_ids.append(int(uid))
        logger.debug(f"Retrieved {len(users_ids)} users")
        return users_ids

    async def get_admins(self) -> List[int]:
        cursor = self.admins.find({})
        admin_ids = []
        async for admin in cursor:
            if 'user_id' not in admin:
                continue
            uid = admin['user_id']
            if isinstance(uid, dict) and '$numberLong' in uid:
                admin_ids.append(int(uid['$numberLong']))
            else:
                admin_ids.append(int(uid))
        logger.debug(f"Retrieved {len(admin_ids)} admins")
        return admin_ids


db = DB()
