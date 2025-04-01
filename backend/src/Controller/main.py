import asyncio
import logging

from src.API.Bots.models import Bot
from src.API.Bots.service import BotService
from src.Bot.BotController import BotController


class Controller:
    enabled_bots = set()  # Используем set вместо dict

    @classmethod
    async def start_bot(cls, bot: Bot):
        if bot.id not in cls.enabled_bots:
            cls.enabled_bots.add(bot.id)
            await BotController.start(bot.id)
            logging.info(f"Bot {bot.id} started.")

    @classmethod
    async def stop_bot(cls, bot: Bot):
        if bot.id in cls.enabled_bots:
            cls.enabled_bots.remove(bot.id)
            await BotController.stop(bot.id)
            logging.info(f"Bot {bot.id} stopped.")


class ControlPanel:
    logger = logging.getLogger(__name__)

    @classmethod
    def start(cls):
        asyncio.create_task(cls.loop())
        cls.logger.debug("Started ControlPanel")

    @classmethod
    async def loop(cls):
        while True:
            try:
                bots = (
                    await BotService.get_all_bots()
                )  # Получаем актуальный список ботов

                active_bot_ids = {
                    bot.id for bot in bots if bot.status
                }  # ID активных ботов в базе
                existing_bot_ids = set(
                    Controller.enabled_bots
                )  # ID уже запущенных ботов

                # Запускаем новых ботов
                new_bots = active_bot_ids - existing_bot_ids
                for bot_id in new_bots:
                    bot = next((b for b in bots if b.id == bot_id), None)
                    if bot:
                        await Controller.start_bot(bot)

                # Останавливаем деактивированных ботов
                stopped_bots = existing_bot_ids - active_bot_ids
                for bot_id in stopped_bots:
                    bot = next((b for b in bots if b.id == bot_id), None)
                    if bot:
                        await Controller.stop_bot(bot)

                await asyncio.sleep(5)  # Пауза между проверками
            except Exception as e:
                cls.logger.error(f"Error in ControlPanel loop: {e}")
