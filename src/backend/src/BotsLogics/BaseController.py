import asyncio
import glob
import logging
import mimetypes
import os
from abc import abstractmethod, ABC

from src.BotsLogics.VK_API.API import API
from src.Bots.service import BotService


class BaseController(ABC):
    logger = logging.getLogger(__name__)
    running_bots = {}
    controller_registry: dict[str, type["BaseController"]] = {}

    def __init__(self, bot):
        self.bot = bot
        self.api = API(bot.token)
        self.group_id = None

    @abstractmethod
    async def loop(self):
        pass

    @classmethod
    def register_controller(cls, key: str):
        def wrapper(controller_class: type["BaseController"]):
            cls.controller_registry[key] = controller_class
            return controller_class

        return wrapper

    @classmethod
    async def start(cls, bot_id: int):
        if bot_id in cls.running_bots:
            cls.logger.info(f"Bot {bot_id} is already running.")
            return

        bot = (await BotService.get_bot(id=bot_id))[0]
        controller_class = cls.controller_registry.get(bot.answers_type)

        if not controller_class:
            cls.logger.warning(
                f"No controller found for answers_type: {bot.answers_type}"
            )
            return

        bot_instance = controller_class(bot)
        bot_instance.group_id = await bot_instance.find_group()

        if bot_instance.group_id != 1:

            async def loop_wrapper():
                try:
                    await bot_instance.loop()
                except asyncio.CancelledError:
                    cls.logger.info(f"Bot {bot_id} loop has been cancelled.")
                except Exception as ex:
                    cls.logger.error(f"Bot {bot_id} loop error: {ex}")
                finally:
                    cls.logger.info(f"Cleaning up bot {bot_id}.")
                    await BotService.update_bot(bot_id=bot_id, status=False)
                    await cls.stop(bot_id=bot_id)

            task = asyncio.create_task(loop_wrapper())
            cls.running_bots[bot_id] = task
            cls.logger.info(f"Bot {bot_id} started.")
        else:
            cls.logger.info(f"Bot {bot_id} not found group.")
            await BotService.update_bot(bot_id, status=False)

    @classmethod
    async def stop(cls, bot_id: int):
        if bot_id in cls.running_bots:
            task = cls.running_bots.pop(bot_id)
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                cls.logger.info(f"Bot {bot_id} stopped.")

    async def find_group(self):
        list_conversation = await self.api.getConversations()
        for conversation in list_conversation:
            if conversation.conversationType == "chat":
                self.logger.debug(conversation.textLastMessage)
                if await self.check_chat(conversation.peerId, self.bot.group_name):
                    return conversation.peerId
        return 1

    async def check_chat(self, peer_id: int, name: str):
        chat = await self.api.getChat(peerId=peer_id)
        self.logger.debug(chat.name)
        return chat.name == name

    @staticmethod
    def find_bot_image(bot_id: int) -> str | None:
        images_dir = os.path.join(os.getcwd(), "images")
        pattern = os.path.join(images_dir, f"{bot_id}.*")
        matched_files = glob.glob(pattern)

        for file_path in matched_files:
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type and mime_type.startswith("image/"):
                return file_path

        return None
