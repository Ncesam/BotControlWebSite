import logging
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase

from bots.Config import config
from bots.Schemas.User import User


class ShopDataBase:
    logger = logging.getLogger(__name__)
    client: AsyncIOMotorClient
    db: AsyncIOMotorDatabase
    collection: AsyncIOMotorCollection

    def __init__(self, bot_id: int):
        self.bot_id = bot_id
        self.client = AsyncIOMotorClient(host=config.MONGODB_HOST, port=config.MONGODB_PORT)
        self.db = self.client[str(self.bot_id)]
        self.collection = self.db['users']

    async def create_new_user(self, user: User) -> int:
        result = await self.collection.insert_one(user.model_dump())
        self.logger.debug(f"In shop {self.bot_id} created new user {user.id}")
        return result.inserted_id

    async def increase_score(self, user_id: int, score: int) -> None:
        await self.collection.update_one(filter={'user_id': user_id}, update={'$inc': {'score': score}})
        self.logger.debug(f"In shop {self.bot_id} increased score {score} to {user_id}")

    async def decrease_score(self, user_id: int, score: int) -> None:
        await self.collection.update_one(filter={'user_id': user_id}, update={'$dec': {'score': score}})
        self.logger.debug(f"In shop {self.bot_id} decreased score {score} to {user_id}")

    async def check_user(self, user_id: int) -> [str, Any] | bool:
        result = await self.collection.find_one(filter={'user_id': user_id})
        if result is None:
            return False
        return result

    @classmethod
    async def drop_table(cls, bot_id: int):
        client = AsyncIOMotorClient(config.MONGODB_HOST, port=config.MONGODB_PORT)
        await client.drop_database(name_or_database=str(bot_id))
        cls.logger.debug(f"Shop {bot_id} dropped")




