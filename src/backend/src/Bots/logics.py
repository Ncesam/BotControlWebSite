import logging
from typing import List

from fastapi import Depends
from starlette.requests import Request
from starlette.responses import Response

from src.Auth.logics import AuthLogics
from src.Bots.models import Bot
from src.Bots.schemas import BotForm, BotParams, BotUpdateForm, Command
from src.Bots.service import BotService
from src.Bots.utils import prepare_nickname_string
from src.Users.logics import UsersLogics
from src.Users.schemas import UserParameters


class BotsLogics:
    logger = logging.getLogger(__name__)

    @classmethod
    async def add_bot(
        cls, request: Request, response: Response, params: BotForm = Depends()
    ):
        await AuthLogics.authenticate_user(request, response)
        user = await UsersLogics.get_user_by_request(request)
        nicknames = params.nicknames
        nicknames = prepare_nickname_string(nicknames)
        bot = Bot(
            token=params.token,
            nicknames=nicknames,
            user_id=user.id,
            user=user,
            title=params.title,
            description=params.description,
            group_name=params.group_name,
            answers_type=params.answers_type,
            text=params.text,
            ads_delay=params.ads_delay
        )
        bot_id = await BotService.add_bot(bot, user)
        return bot_id

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
    async def add_command(cls, id: int, request: Request, response: Response, commands: List[Command]):
        await AuthLogics.authenticate_user(request, response)
        commandsList = [command.model_dump() for command in commands]
        await BotService.update_bot(bot_id=id, commands=commandsList)
        return id
    
    @classmethod
    async def update_bot(
        cls, request: Request, response: Response, params: BotUpdateForm = Depends()
    ):
        await AuthLogics.authenticate_user(request, response)
        nicknames = params.nicknames
        cls.logger.debug(nicknames)
        cls.logger.debug(params)
        nicknames = prepare_nickname_string(nicknames)
        await BotService.update_bot(
            params.id,
            token=params.token,
            nicknames=nicknames,
            title=params.title,
            description=params.description,
            group_name=params.group_name,
            answers_type=params.answers_type,
            text=params.text,
            ads_delay=params.ads_delay
        )
        return params.id

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
