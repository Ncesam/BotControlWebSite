from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    JWT_ALG: str
    JWT_KEY: str
    JWT_EXP: int

    REFRESH_TOKEN_KEY: str
    REFRESH_TOKEN_EXP: int

    class Config:
        env_file = ".env"
        extra = "ignore"


auth_settings = AuthConfig()
