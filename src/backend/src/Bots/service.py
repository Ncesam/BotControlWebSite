import logging

from src.Auth.models import User
from src.Bots.exceptions import BotNotFound, BotErrorAdd
from src.Bots.models import Bot
from src.DataBase import BaseDTO


class BotService(BaseDTO):
    model = Bot
    logger = logging.getLogger(__name__)

    @classmethod
    async def get_bot(cls, **filters):
        bots = await cls.select_by_filters(**filters)
        if not bots:
            raise BotNotFound(filters)
        return bots

    @classmethod
    async def get_all_bots(cls):
        bots = await cls.select_all()
        return bots

    @classmethod
    async def add_bot(cls, bot_data: Bot, user: User):
        bot_data.user = user
        response = await cls.insert(bot_data)
        if not response:
            raise BotErrorAdd()
        return response

    @classmethod
    async def delete_bot(cls, bot_id: int):
        await cls.delete_by_filters(id=bot_id)

    @classmethod
    async def update_bot(cls, bot_id: int, **update_data):
        await cls.update(update_data, id=bot_id)
