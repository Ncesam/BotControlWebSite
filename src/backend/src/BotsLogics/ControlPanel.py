import asyncio
import logging

from src.BotsLogics.Utils import auto_register_controllers
from src.Bots.service import BotService

auto_register_controllers("src.BotsLogics.Controllers")

from src.BotsLogics.BaseController import BaseController


class ControlPanel:
    logger = logging.getLogger(__name__)

    @classmethod
    def start(cls):
        asyncio.create_task(cls.loop())
        cls.logger.info("Started ControlPanel")

    @classmethod
    async def loop(cls):
        while True:
            try:
                bots = await BotService.get_all_bots()
                active_bot_ids = {bot.id for bot in bots if bot.status}
                existing_bot_ids = set(BaseController.running_bots)

                new_bots = active_bot_ids - existing_bot_ids
                for bot_id in new_bots:
                    bot = next((b for b in bots if b.id == bot_id), None)
                    if bot:
                        await BaseController.start(bot.id)

                stopped_bots = existing_bot_ids - active_bot_ids
                for bot_id in stopped_bots:
                    bot = next((b for b in bots if b.id == bot_id), None)
                    if bot:
                        await BaseController.stop(bot.id)

                await asyncio.sleep(10)

            except Exception as e:
                cls.logger.exception(f"Error in ControlPanel loop: {e}")
                await asyncio.sleep(3)
