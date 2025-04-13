import logging

from src.Auth.exceptions import UserNotFound, UserAlreadyExists
from src.Auth.models import User
from src.Auth.schemas import UserDB
from src.DataBase import BaseDTO


class UserService(BaseDTO):
    model = User
    logger = logging.getLogger(__name__)

    @classmethod
    async def get_user(cls, with_bots: bool = False, **filters):
        user: User = (
            await cls.select_one_or_none(**filters)
            if not with_bots
            else await cls.select_with_some("bots", **filters)
        )
        if not user:
            raise UserNotFound(filters)
        return user

    @classmethod
    async def add_user(cls, user_data: User):
        response = await cls.insert(user_data)
        if not response:
            raise UserAlreadyExists()

    @classmethod
    async def delete_user(cls, user_data: UserDB):
        await cls.delete_by_filters(email=user_data.email)

    @classmethod
    async def update_user(cls, user_email: str, **update_data):
        await cls.update(email=user_email, new_data={**update_data})
