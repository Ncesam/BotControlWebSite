import asyncio

import random
import re

from src.Bots.BaseController import BaseController

answers_storage = {r"бусь а": "Заклинание А", r"бусь в": "Заклинание В"}


@BaseController.register_controller("baf")
class StorageController(BaseController):
    async def loop(self):
        processed_messages = set()

        try:
            while True:
                messages = await self.api.getHistoryMessages(peerId=self.group_id)

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
