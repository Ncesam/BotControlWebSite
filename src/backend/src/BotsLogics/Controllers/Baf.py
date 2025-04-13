import asyncio

import random
import re

from src.BotsLogics.BaseController import BaseController

answers_storage = {
    r"/баф а": "благославение атаки",
    r"/баф з": "благославение защиты",
    r"/баф у": "благославение удачи",
    r"/баф ч": "благославение человека",
    r"/баф г": "благославение гоблина",
    r"/баф н": "благославение нежити",
    r"/баф э": "благославение эльфа",
    r"/баф м": "благославение гнома",
    r"/баф д": "благославение демона",
    r"/баф о": "благославение орка",
    r"/баф л": "благославение неудачи",
    r"/баф б": "благославение боли",
    r"/баф ю": "благославение добычи",
    r"/баф и": "благославение очищение",
    r"/баф с": "благославение света",
    r"/баф т": "благославение огня",
    r"/бафы": """✨Список бафов:
а - атаки
з - защиты
у - удачи
ч - человека
г - гоблина
н - нежити
э - эльфа
м - гнома
д - демона
о - орка
л - неудачи
б - боли
ю - добычи
и - очищение
с - света
т - огня""",
}


@BaseController.register_controller("baf")
class StorageController(BaseController):
    async def loop(self):
        processed_messages = set()

        try:
            messages = await self.api.getHistoryMessages(
                peerId=self.group_id, last_message_id=-1
            )
            while True:
                for message in messages:
                    if message.messageId in processed_messages:
                        continue

                    if not await self.check_user(message.peerId):
                        continue
                    response = self.choose_answer(message.text)
                    if response:
                        result = await self.api.sendMessage(
                            peerId=self.group_id,
                            reply_to=message.messageId,
                            text=response,
                        )
                        if isinstance(result, dict) and "response" in result:
                            processed_messages.add(result["response"])

                            # Отмечаем исходное сообщение как обработанное
                    processed_messages.add(message.messageId)

                    await asyncio.sleep(random.uniform(1.0, 3.0))

                await asyncio.sleep(random.uniform(1.0, 3.0))

                if len(processed_messages) > 1000:
                    processed_messages.clear()
                messages = await self.api.getHistoryMessages(
                    peerId=self.group_id, last_message_id=-1
                )
        except Exception as e:
            self.logger.error(f"Ошибка в StorageController: {e}")

    def choose_answer(self, message: str):
        """Выбирает ответ, подставляя переменные, если это необходимо"""
        for pattern, response_template in answers_storage.items():
            if re.fullmatch(pattern, message, flags=re.IGNORECASE):
                return response_template
        return None

    async def get_user_name(self, user_id: int):
        """Получаем имя пользователя по ID"""
        try:
            return await self.api.getUser(user_id)
        except Exception as e:
            self.logger.error(f"Ошибка при получении имени пользователя {user_id}: {e}")
            return None

    async def check_user(self, peerId: int):
        """Проверяем, является ли пользователь разрешённым"""
        if peerId < 0:
            return False
        user = await self.get_user_name(peerId)
        if user and user.full_name not in self.bot.nicknames:
            self.logger.info(f"User {user.full_name} не входит в список разрешённых.")
            return False
        return True
