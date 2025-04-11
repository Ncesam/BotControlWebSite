import asyncio
import random
import re

import aiohttp
import emoji

from bots.BaseController import BaseController
from shared.NoSQL import ShopDataBase
from bots.Schemas.User import User
from bots.VK_API.Schema import Message

answers_storage = {
    r"{first_name}, получено: {item} от игрока {owner_item}": "put_handler",
    r"{first_name}, взять {item} - {n}": "take_handler",
    r"{first_name}, взять {item}": "take_handler",
    r"{first_name}": "random_quote_handler"
}
answers = {
    "not enough": '''На вашем счету недостаточно средств.
    Ваш счет: {score}.''',
    "increase": '''Пополняем на {increase_score}. 
    Ваш счет: {score}.''',
    "decrease": '''Списываем {decrease_score}.
    Ваш счет: {score}'''
}


@BaseController.register_controller("shop")
class StorageController(BaseController):
    async def loop(self):
        self.database = ShopDataBase(self.bot.id)
        self.bot_user = await self.api.getMe()
        self.first_name = self.bot_user.firstName
        self.last_name = self.bot_user.lastName
        self.sign = self.bot.sign
        processed_messages = set()

        try:
            while True:
                messages = await self.api.getHistoryMessages(peerId=self.group_id)

                for message in messages:
                    if message.messageId in processed_messages:
                        continue

                    if not await self.check_user(message.peerId):
                        continue
                    await self.run_logic(message)

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

    async def create_user(self, peer_id: int):
        user = await self.get_user_name(peer_id)
        await self.database.create_new_user(User(user.userId, user.firstName, user.lastName, 0))

    async def random_quote_handler(self, message: Message, groups: dict):
        response = "Все хотят быть человеком пауком, но никто не хочет быть Питером Паркером."
        await self.api.sendMessage(
            peerId=self.group_id,
            reply_to=message.messageId,
            text=response
        )

    async def put_handler(self, message: Message, groups: dict):
        item = groups.get("item", "неизвестно")
        n = int(groups.get("n", 1))

        user = await self.database.check_user(message.peerId)
        if not user:
            await self.create_user(message.peerId)
            user = await self.database.check_user(message.peerId)

        user.score += n

        response = answers["increase"].format(
            increase_score=n,
            score=user.score
        )
        await self.api.sendMessage(
            peerId=self.group_id,
            reply_to=message.messageId,
            text=response
        )

    async def find_item(self, item: str):
        async with aiohttp.ClientSession() as session:
            url = f'https://vip3.activeusers.ru/app.php?act=item&id={item}&sign={self.sign}&vk_access_token_settings=&vk_app_id=7055214&vk_are_notifications_enabled=0&vk_group_id=182985865&vk_is_app_user=1&vk_is_favorite=0&vk_language=ru&vk_platform=desktop_web&vk_ref=other&vk_ts=1744217261&vk_user_id={self.bot_user.userId}&vk_viewer_group_role=member&back=act:shop;cat:348',

    async def take_handler(self, message: Message, groups: dict):
        item = groups.get("item", "неизвестно")
        try:
            n = int(groups.get("n", 1))
        except ValueError:
            n = 1

        user = await self.database.check_user(message.peerId)
        if not user:
            await self.create_user(message.peerId)
            user = await self.database.check_user(message.peerId)

        if user.score < n:
            response = answers["not enough"].format(score=user.score)
        else:
            user.score -= n
            await self.database.update_user(user)

            response = answers["decrease"].format(
                decrease_score=n,
                score=user.score
            )
        self.api.

    async def run_logic(self, message: Message):
        for pattern, handler_name in answers_storage.items():
            regex_pattern = self.compile_pattern(pattern)
            match = re.match(regex_pattern, message.text, flags=re.IGNORECASE)

            if match:
                groups = match.groupdict()
                groups = {k: self.clean_text(v) for k, v in groups.items()}
                handler = getattr(self, handler_name, None)

                if handler:
                    await handler(message, groups)
                else:
                    self.logger.warning(f"Handler {handler_name} не найден")
                return
            result = await self.api.sendMessage(
                peerId=self.group_id,
                reply_to=message.messageId,
                text=response,
            )
