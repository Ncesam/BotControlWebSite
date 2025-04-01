import logging

from starlette.requests import Request
from starlette.responses import Response

from src.API.Auth.logics import AuthLogics
from src.API.Bots.models import Bot
from src.API.Bots.schemas import BotForm, BotParams, BotUpdateForm
from src.API.Bots.service import BotService
from src.API.Bots.utils import prepare_nickname_string
from src.API.Users.logics import UsersLogics
from src.API.Users.schemas import UserParameters


class BotsLogics:
    logger = logging.getLogger(__name__)

    @classmethod
    async def add_bot(cls, bot_data: BotForm, request: Request, response: Response):
        await AuthLogics.authenticate_user(request, response)
        user = await UsersLogics.get_user_by_request(request)
        nicknames = bot_data.nicknames
        nicknames = prepare_nickname_string(nicknames)
        bot = Bot(
            token=bot_data.token,
            nicknames=nicknames,
            user_id=user.id,
            user=user,
            title=bot_data.title,
            description=bot_data.description,
            group_name=bot_data.group_name,
            answers_type=bot_data.answers_type,
        )
        await BotService.add_bot(bot, user)

    @classmethod
    async def get_bots(cls, request: Request, response: Response):
        await AuthLogics.authenticate_user(request, response)
        user = await UsersLogics.get_user_by_request(request)
        user_bots = await UsersLogics.get_users(
            UserParameters(user_ids=[user.id], fields=["bots"])
        )
        return user_bots

    @classmethod
    async def start_bots(
        cls, request: Request, bot_params: BotParams, response: Response
    ):
        await AuthLogics.authenticate_user(request, response)
        return await cls.__switch_status(request, response, bot_params, True)

    @classmethod
    async def delete_bot(cls, bot_id: int, request: Request, response: Response):
        await AuthLogics.authenticate_user(request, response)
        await BotService.delete_bot(bot_id)
        return f"Bot {bot_id} deleted"

    @classmethod
    async def update_bot(cls, bot: BotUpdateForm, request: Request, response: Response):
        await AuthLogics.authenticate_user(request, response)
        nicknames = bot.nicknames
        nicknames = prepare_nickname_string(nicknames)
        await BotService.update_bot(
            bot.id,
            token=bot.token,
            nicknames=nicknames,
            title=bot.title,
            description=bot.description,
            group_name=bot.group_name,
            answers_type=bot.answers_type,
        )
        return f"Bot {bot.id} updated"

    @classmethod
    async def stop_bots(
        cls, request: Request, bot_params: BotParams, response: Response
    ):
        await AuthLogics.authenticate_user(request, response)
        return await cls.__switch_status(request, response, bot_params, False)

    @classmethod
    async def __switch_status(
        cls, request: Request, response: Response, bot_params: BotParams, status: bool
    ):
        user_bots = await cls.get_bots(request, response)
        started_bots = {}
        for bot_id in bot_params.bot_ids:
            started_bots[bot_id] = "Not"
        for user_bot in user_bots["items"][0]["bots"]:
            for bot_id in bot_params.bot_ids:
                if user_bot.id == bot_id:
                    started_bots[bot_id] = "Ok"
                    await BotService.update_bot(bot_id, status=status)
        return started_bots
