from typing import List, Literal, Union

from pydantic import BaseModel
from backend.src.Bots.models import Bot
from src.backend.src.Bots.service import BotService
from src.backend.src.Config import config
from faststream.rabbit import fastapi, RabbitQueue
class Message(BaseModel):
    type: Literal["Get all", "Update", "Response"]
    body: Union[dict, list, str, int]
    
rabbit_router = fastapi.RabbitRouter(config.RABBITMQ_URL)

backend_queue = RabbitQueue("Backend")
bots_queue = RabbitQueue("Bots")


@rabbit_router.subscriber(backend_queue)
@rabbit_router.publisher(bots_queue)
async def handler_backend(msg: Message):
    response = Message(type="Response")

    if msg.type == "Get all":
        bots: List[Bot] = await BotService.get_all_bots()
        body = {
            "status": 200,
            "items": bots
        }

    elif msg.type == "Update":
        await BotService.update_bot(msg.body, status=False)
        body = {
            "status": 200
        }

    else:
        body = {
            "status": "404"
        }
        
    await rabbit_router.broker.publish(message=response, queue=bots_queue)


