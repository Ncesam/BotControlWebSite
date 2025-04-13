import logging
from datetime import datetime, timedelta

import bcrypt
import jwt
from sqlalchemy.exc import SQLAlchemyError
from starlette.requests import Request

from src.Auth.config import auth_settings
from src.Auth.exceptions import JWTNotFound, JWTError, JWTExpired, ReLogin
from src.Auth.service import UserService
from src.Exceptions import ServerError


class JWT:
    logger = logging.getLogger(__name__)

    @classmethod
    def hash_password_generate(cls, password: str) -> str:
        """Generate a password hash"""
        try:
            return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        except Exception as e:
            cls.logger.error(f"Error while hashing password: {e}")
            raise ServerError()

    @classmethod
    def verify_passwords(cls, password: str, hashed_password: str) -> bool:
        """Verify if the password matches the stored hash"""
        return bcrypt.checkpw(password.encode(), hashed_password.encode())

    @classmethod
    def get_access_token(cls, request: Request) -> str:
        raw_access_token = request.cookies.get("Authorization")
        if not raw_access_token:
            raise JWTNotFound()
        access_token = raw_access_token.split(" ")[1]
        return access_token

    @classmethod
    async def create_access_token(cls, user_email: str, refresh_token: str) -> str:
        """Create an access token"""
        await cls.check_refresh_token(refresh_token)
        payload = {
            "email": user_email,
            "exp": datetime.utcnow() + timedelta(minutes=auth_settings.JWT_EXP),
        }
        try:
            access_token = jwt.encode(
                payload, auth_settings.JWT_KEY, algorithm=auth_settings.JWT_ALG
            )
            return access_token
        except jwt.PyJWTError as e:
            cls.logger.error(f"Error while creating access token: {e}")
            raise JWTError()

    @classmethod
    def get_user_email(cls, access_token: str) -> str:
        """Get the user's email"""

        payload = jwt.decode(
            access_token, auth_settings.JWT_KEY, algorithms=[auth_settings.JWT_ALG]
        )
        return payload["email"]

    @classmethod
    def check_access_token(cls, access_token: str) -> bool:
        """Validate the access token"""
        try:
            payload = jwt.decode(
                access_token,
                key=auth_settings.JWT_KEY,
                algorithms=[auth_settings.JWT_ALG],
            )
            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
                cls.logger.debug("Access JWT has expired")
                raise JWTExpired()
            return True
        except jwt.ExpiredSignatureError:
            cls.logger.debug("Access JWT has expired")
            raise JWTExpired()
        except jwt.PyJWTError:
            cls.logger.debug("Invalid JWT verification")
            raise JWTError()

    @classmethod
    def create_refresh_token(cls, user_email: str) -> str:
        """Create a refresh token"""
        payload = {
            "email": user_email,
            "exp": datetime.utcnow() + timedelta(days=auth_settings.REFRESH_TOKEN_EXP),
        }
        try:
            return jwt.encode(
                payload,
                auth_settings.REFRESH_TOKEN_KEY,
                algorithm=auth_settings.JWT_ALG,
            )
        except jwt.PyJWTError as e:
            cls.logger.error(f"Error while creating refresh token: {e}")
            raise ServerError()

    @classmethod
    async def add_refresh_token(cls, user_email: str, refresh_token: str):
        """Add the refresh token to the user"""
        try:
            await UserService.update_user(
                user_email=user_email, refresh_token=refresh_token
            )
        except SQLAlchemyError as e:
            cls.logger.error(f"Error updating refresh token: {e}")
            raise

    @classmethod
    async def delete_refresh_token(cls, user_email: str):
        """Delete the refresh token"""
        await UserService.update_user(user_email=user_email, refresh_token=None)

    @classmethod
    async def check_refresh_token(cls, refresh_token: str) -> bool:
        """Validate the refresh token"""
        try:
            payload = jwt.decode(
                refresh_token,
                key=auth_settings.REFRESH_TOKEN_KEY,
                algorithms=[auth_settings.JWT_ALG],
            )
            if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
                cls.logger.debug("Refresh JWT has expired")
                raise ReLogin()
            return True
        except jwt.ExpiredSignatureError:
            cls.logger.debug("Refresh JWT has expired")
            raise ReLogin()
        except jwt.PyJWTError:
            cls.logger.debug("Invalid Refresh JWT verification")
            raise ReLogin()

    @classmethod
    async def get_refresh_token(cls, user_email: str) -> str:
        """Retrieve the user's refresh token"""
        user = await UserService.get_user(email=user_email)
        refresh_token = user.refresh_token
        if await cls.check_refresh_token(refresh_token):
            cls.logger.debug("Refresh JWT is valid")
            return refresh_token
        cls.logger.debug("Refresh JWT is invalid")
        raise ReLogin()

    @classmethod
    async def update_refresh_token(cls, user_email: str) -> str:
        """Update the refresh token"""
        refresh_token = cls.create_refresh_token(user_email)
        await cls.add_refresh_token(user_email, refresh_token)
        return refresh_token

    @classmethod
    def get_user_email_by_refresh_token(cls, refresh_token: str):
        payload = jwt.decode(
            refresh_token,
            key=auth_settings.REFRESH_TOKEN_KEY,
            algorithms=[auth_settings.JWT_ALG],
        )
        return payload["email"]
