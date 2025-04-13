import logging

from starlette.requests import Request
from starlette.responses import Response

from src.Auth.dependencies import JWT
from src.Auth.exceptions import PasswordNotMatch
from src.Auth.schemas import User
from src.Auth.models import User as UserDB
from src.Auth.service import UserService
from src.Users.logics import UsersLogics


class AuthLogics:
    logger = logging.getLogger(__name__)

    @classmethod
    async def login_user(cls, user_data: User) -> tuple[str, str]:
        """Authenticate the user"""
        user = await cls.check_user(user_data)

        refresh_token = JWT.create_refresh_token(user.email)
        await JWT.add_refresh_token(user.email, refresh_token)

        access_token = await JWT.create_access_token(user_data.email, refresh_token)
        cls.logger.debug("User successfully logged in")
        return access_token, refresh_token

    @classmethod
    async def register_user(cls, user_data: User) -> tuple[str, str]:
        hashed_password = JWT.hash_password_generate(user_data.password)
        refresh_token = JWT.create_refresh_token(user_data.email)
        await UserService.add_user(
            UserDB(
                email=user_data.email,
                nickname=user_data.email,
                hashed_password=hashed_password,
                refresh_token=refresh_token,
            )
        )

        access_token = await JWT.create_access_token(user_data.email, refresh_token)
        cls.logger.debug("User successfully registered")
        return access_token, refresh_token

    @classmethod
    async def check_user(cls, user_data: User):
        """Check if the user exists and the password is valid"""
        user = await UserService.get_user(email=user_data.email)

        if not JWT.verify_passwords(user_data.password, user.hashed_password):
            cls.logger.debug(f"Incorrect password for {user_data.email}")
            raise PasswordNotMatch()

        cls.logger.debug(f"User {user_data.email} passed verification")
        return user

    @classmethod
    async def me(cls, request: Request, response: Response):
        user = await UsersLogics.get_user_by_request(request)
        access_token, refresh_token = await cls.refresh_jwt(request)
        return user.email, access_token, refresh_token

    @classmethod
    async def authenticate_user(cls, request: Request, response: Response):
        AuthLogics.check_user_request(request)
        access_token, refresh_token = await AuthLogics.refresh_jwt(request)
        response.set_cookie(
            key="Authorization",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=3600,
        )

    @classmethod
    def check_user_request(cls, request: Request):
        access_token = JWT.get_access_token(request)
        JWT.check_access_token(access_token)

    @classmethod
    async def refresh_jwt(cls, request: Request):
        user = await UsersLogics.get_user_by_request(request)
        access_token = await JWT.create_access_token(user.email, user.refresh_token)
        return access_token, user.refresh_token

    @classmethod
    async def logout_user(cls, request: Request, response: Response):
        """Logout the user"""
        access_token = JWT.get_access_token(request)
        user_email = JWT.get_user_email(access_token)
        user = await UserService.get_user(email=user_email)
        await JWT.delete_refresh_token(user.email)
        response.delete_cookie("Authorization")
        cls.logger.debug("User successfully logged out")
