from src.backend.src.Config import config
from faststream.rabbit import fastapi

rabbit_router = fastapi.RabbitRouter(config.RABBITMQ_URL)


@rabbit_router.subscriber(queue="Bot")
async def get_all_bots(msg: str):
