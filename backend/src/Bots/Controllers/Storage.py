import asyncio
import random
import re

import emoji

from src.Bots.BaseController import BaseController

answers_storage = {
    r"{first_name}, получено {item} от {owner_item}": "Положить {item} - 1 штук",
    r"{first_name}, взять {item}": "Заклинание В",
}


@BaseController.register_controller("storage")
class StorageController(BaseController):
    async def loop(self):
        self.bot_user = await self.api.getMe()
        self.first_name = self.bot_user.firstName
        self.last_name = self.bot_user.lastName
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

                    processed_messages.add(message.messageId)

                    await asyncio.sleep(random.uniform(1.0, 3.0))

                await asyncio.sleep(random.uniform(1.0, 3.0))

                if len(processed_messages) > 1000:
                    processed_messages.clear()

        except Exception as e:
            self.logger.error(f"Ошибка в StorageController: {e}")

    def choose_answer(self, message: str):
        for pattern, response_template in answers_storage.items():
            regex_pattern = self.compile_pattern(pattern)
            match = re.match(regex_pattern, message, flags=re.IGNORECASE)
            if match:
                groups = match.groupdict()

                item_clean = self.clean_text(groups.get("item", ""))
                groups["item"] = item_clean

                return response_template.format(**groups)

        return None

    def compile_pattern(self, pattern: str) -> str:
        # Подставляем first_name и last_name
        pattern = pattern.replace("{first_name}", re.escape(self.first_name))
        pattern = pattern.replace("{last_name}", re.escape(self.last_name))

        # Превращаем переменные в именованные группы
        return re.sub(r"{(\w+)}", r"(?P<\1>.+)", pattern)

    def clean_text(self, text: str) -> str:
        # Убираем emoji и приводим к нижнему регистру
        return emoji.replace_emoji(text, replace="").strip().lower()

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
