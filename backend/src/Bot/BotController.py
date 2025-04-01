import asyncio
import logging
import re

from src.API.Bots.service import BotService
from src.VK_API.API import API

answers_storage = {
}
answers_baf = {}


class BotController:
    logger = logging.getLogger(__name__)
    running_bots = {}

    @classmethod
    async def start(cls, bot_id: int):
        if bot_id in cls.running_bots:
            cls.logger.info(f"Bot {bot_id} is already running.")
            return

        bot_instance = BotController()
        bot_instance.bot = (await BotService.get_bot(id=bot_id))[0]
        bot_instance.api = API(bot_instance.bot.token)
        bot_instance.group_id = await bot_instance.find_group()

        if bot_instance.group_id != 1:
            loop = asyncio.get_running_loop()
            task = loop.create_task(bot_instance.loop(bot_id))
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

    async def loop(self, bot_id: int):
        processed_messages = set()

        try:
            while True:
                messages = await self.api.getHistoryMessages(peerId=self.group_id)

                for message in messages:
                    if message.messageId in processed_messages:
                        continue
                    if not await self.check_user(message.peerId):
                        continue

                    # 🔹 Проверяем, есть ли имя в списке разрешённых

                    response = self.choose_answer(message.text)
                    if response:
                        messageId = await self.api.sendMessage(
                            self.group_id, message.messageId, response
                        )
                        processed_messages.add(messageId["response"])
                    self.logger.debug(message.messageId)
                    processed_messages.add(message.messageId)
                    await asyncio.sleep(3)
                await asyncio.sleep(3)
                if len(processed_messages) > 1000:
                    processed_messages.clear()
        except asyncio.CancelledError:
            self.logger.info(f"Bot {bot_id} loop has been cancelled.")
        except Exception as ex:
            self.logger.error(f"Bot {bot_id} loop error: {ex}")
        finally:
            self.logger.info(f"Cleaning up bot {bot_id}.")
            await BotService.update_bot(bot_id=bot_id, status=False)

    def choose_answer(self, message: str):
        """Выбирает ответ с обработкой переменных"""
        if self.bot.answers_type == "storage":
            answers = answers_storage
        elif self.bot.answers_type == "baf":
            answers = answers_baf
        else:
            return None

        for pattern, response_template in answers.items():
            match = self.match_pattern(pattern, message)
            if match:
                response = response_template.format(**match)
                return response
        return "Я не понял ваш вопрос."

    def match_pattern(self, pattern: str, message: str):
        """Проверяет, соответствует ли сообщение шаблону, и извлекает переменные"""
        pattern_regex = re.sub(r"\{(\w+)\}", r"(?P<\1>.+)", pattern)
        match = re.match(pattern_regex, message, re.IGNORECASE)
        return match.groupdict() if match else None

    async def find_group(self):
        list_conversation = await self.api.getConversations()
        for conversation in list_conversation:
            if conversation.conversationType == "chat":
                self.logger.debug(conversation.textLastMessage)
                if await self.check_chat(conversation.peerId, self.bot.group_name):
                    return conversation.peerId
        return 1

    async def get_user_name(self, user_id: int):
        try:
            return await self.api.getUser(user_id)
        except Exception as e:
            self.logger.error(f"Ошибка при получении имени пользователя {user_id}: {e}")
            return ""

    async def check_group(self, peer_id: int, name: str):
        group = await self.api.getGroup(peerId=peer_id)
        return group.name == name

    async def check_chat(self, peer_id: int, name: str):
        chat = await self.api.getChat(peerId=peer_id)
        self.logger.debug(chat.name)
        return chat.name == name

    async def check_user(self, peerId: int):
        if peerId < 0:
            return False
        user = await self.get_user_name(peerId)
        if user.full_name not in self.bot.nicknames:
            self.logger.info(f"User {user.full_name} is not allowed. Ignoring message.")
            return False
        return True
