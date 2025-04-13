import logging
from typing import List

from starlette.requests import Request

from src.Auth.dependencies import JWT
from src.Auth.models import User
from src.Auth.service import UserService
from src.Users.schemas import UserParameters


class UsersLogics:
    logger = logging.getLogger(__name__)

    @classmethod
    async def get_user_by_request(cls, request: Request):
        access_token = JWT.get_access_token(request)
        user_email = JWT.get_user_email(access_token)
        user = await UserService.get_user(email=user_email)
        return user

    @classmethod
    async def get_user_by_refresh_token(cls, refresh_token: str):
        await JWT.check_refresh_token(refresh_token)
        user_email = JWT.get_user_email_by_refresh_token(refresh_token)
        user = await UserService.get_user(email=user_email)
        return user

    @classmethod
    async def get_users(cls, user_parameters: UserParameters):
        result = {"items": []}
        for user_id in user_parameters.user_ids:
            user_info = await cls.__get_user_info(
                user_id=user_id, fields=user_parameters.fields
            )
            result["items"].append(user_info)
        return result

    @classmethod
    async def __get_user_info(cls, user_id: int, fields: List[str]):
        user = (
            await UserService.get_user(with_bots=True, id=user_id)
            if "bots" in fields or "All" in fields
            else await UserService.get_user(id=user_id)
        )
        filtered_data = cls.__get_filtred_data(fields, user)
        return filtered_data

    @classmethod
    def __get_filtred_data(cls, fields: List[str], data: User):
        result = {}

        def filter_iter(fields: list):
            for field in fields:
                if field == "user_id":
                    result[field] = data.id
                    continue
                elif field == "bots":
                    result[field] = [Bot for Bot in data.bots]
                else:
                    result[field] = getattr(data, field)

        if "All" in fields:
            filter_iter(["user_id", "nicknames", "bots", "email"])
        else:
            filter_iter(fields)

        return result
