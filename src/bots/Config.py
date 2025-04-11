from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ADS_DELAY: int
    DELAY: int
    MONGODB_HOST: str
    MONGODB_PORT: int

    class Config:
        env_file = ".env"
        extra = "ignore"


config = Config()


