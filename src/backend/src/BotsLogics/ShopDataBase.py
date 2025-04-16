import logging
from typing import Any, Union

from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from src.BotsLogics.Config import config
from src.BotsLogics.Schemas.Price import Price
from src.BotsLogics.Schemas.User import User


class ShopDataBase:
    logger = logging.getLogger(__name__)
    client: AsyncIOMotorClient
    db: AsyncIOMotorDatabase
    collection: AsyncIOMotorCollection

    def __init__(self, bot_id: int):
        self.bot_id = bot_id
        self.client = AsyncIOMotorClient(
            host=config.MONGODB_HOST, port=config.MONGODB_PORT
        )
        self.db = self.client[str(self.bot_id)]
        self.collection = self.db["users"]

    async def create_new_user(self, user: User) -> int:
        result = await self.collection.insert_one(user.model_dump())
        self.logger.debug(f"In shop {self.bot_id} created new user {user.id}")
        return result.inserted_id

    async def increase_score(self, user_id: int, score: int) -> None:
        await self.collection.update_one(
            filter={"id": user_id}, update={"$inc": {"score": score}}
        )
        self.logger.debug(f"In shop {self.bot_id} increased score {score} to {user_id}")

    async def decrease_score(self, user_id: int, score: int) -> None:
        await self.collection.update_one(
            filter={"id": user_id}, update={"$inc": {"score": (-score)}}
        )
        self.logger.debug(f"In shop {self.bot_id} decreased score {score} to {user_id}")

    async def check_user(self, user_id: int) -> Union[Any, bool]:
        result = await self.collection.find_one(filter={"id": user_id})
        if result is None:
            return False
        return result

    @classmethod
    async def drop_table(cls, bot_id: int):
        client = AsyncIOMotorClient(config.MONGODB_HOST, port=config.MONGODB_PORT)
        await client.drop_database(name_or_database=str(bot_id))
        cls.logger.debug(f"Shop {bot_id} dropped")


class PriceDataBase:
    logger = logging.getLogger(__name__)
    client: AsyncIOMotorClient
    db: AsyncIOMotorDatabase
    collection: AsyncIOMotorCollection

    def __init__(self):
        self.client = AsyncIOMotorClient(
            host=config.MONGODB_HOST, port=config.MONGODB_PORT
        )
        self.db = self.client["Price"]
        self.collection = self.db["Price"]

    async def add_all_item(self):
        # First, delete all existing documents in the collection
        await self.collection.delete_many({})

        # Create a list to hold the new data to insert
        data_to_insert = [
            {
                "id": i,
                "name": "",
                "hign_price": 0,  # Adjust the price range as needed
                "low_price": 0,
                "average_price": 0,
            }
            for i in range(13580, 19000)
        ]

        # Insert all the new data
        await self.collection.insert_many(data_to_insert)
        self.logger.debug(f"Inserted {len(data_to_insert)} new items.")

    async def get_all_price(self):
        data = await self.collection.find().to_list(None)
        return data

    async def get_item_price(self, item_name: str):
        item = await self.collection.find_one({"name": item_name})
        return item

    async def update_item(self, item_id: int, price: Price, title: str):
        await self.collection.update_one(
            {"id": item_id}, {"$set": {**price.model_dump(), "name": title}}
        )


price_database = PriceDataBase()
