import asyncio
import random
import re

import emoji

from src.BotsLogics.BaseController import BaseController
from src.BotsLogics.Schemas.User import User
from src.BotsLogics.ShopDataBase import ShopDataBase, price_database
from src.BotsLogics.VK_API.Schema.Message import Message

answers_storage = {
    r"передать {item} - {n}": "put_handler",
    r"{title}, взять {item} - {n}": "take_handler",
    r"{title}, взять {item}": "take_handler",
    r"{title}, мой баланс": "balance",
    r"{title}": "random_quote_handler",
}
answers = {
    "not enough": """На вашем счету недостаточно средств.
Ваш счет: {score}.""",
    "increase": """Пополняем на {increase_score}. 
Ваш счет: {score}.""",
    "decrease": """Списываем {decrease_score}.
Ваш счет: {score}""",
    "balance": "Ваш баланс равен: {score}",
}


@BaseController.register_controller("shop")
class StorageController(BaseController):
    async def loop(self):
        self.database = ShopDataBase(self.bot.id)
        self.bot_user = await self.api.getMe()
        self.first_name = self.bot_user.firstName
        self.last_name = self.bot_user.lastName
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
                    await self.run_logic(message)

                    processed_messages.add(message.messageId)

                    await asyncio.sleep(random.uniform(1.0, 3.0))

                await asyncio.sleep(random.uniform(1.0, 3.0))

                if len(processed_messages) > 1000:
                    processed_messages.clear()
                messages = await self.api.getHistoryMessages(
                    peerId=self.group_id, last_message_id=-1
                )

        except Exception as e:
            self.logger.error(f"Ошибка в StorageController: {e}", exc_info=True)

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
        pattern = pattern.replace("{title}", re.escape(self.bot.title))
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
        await self.database.create_new_user(
            User(
                id=user.userId,
                first_name=user.firstName,
                last_name=user.lastName,
                score=0,
            )
        )

    async def random_quote_handler(self, message: Message, groups: dict):
        response = (
            "Все хотят быть человеком пауком, но никто не хочет быть Питером Паркером."
        )
        await self.api.sendMessage(
            peerId=self.group_id, reply_to=message.messageId, text=response
        )

    async def put_handler(self, message: Message, groups: dict):
        if message.reply.peerId == self.bot_user.userId:
            item = groups.get("item", "неизвестно")
            n = int(groups.get("n", 1))

            user = await self.database.check_user(message.peerId)
            if not user:
                await self.create_user(message.peerId)
                user = await self.database.check_user(message.peerId)
            item = await price_database.get_item_price(item.capitalize())
            if item:
                price = item["average_price"] * n
                user["score"] += price
                await self.database.increase_score(user_id=user["id"], score=price)
                response = answers["increase"].format(
                    increase_score=price, score=user["score"]
                )
                await self.api.sendMessage(
                    peerId=self.group_id, reply_to=message.messageId, text=response
                )
                put_response = f"Положить {item['name']} - {n} штук"
                await self.api.sendMessage(peerId=self.group_id, text=put_response)
            else:
                await self.api.sendMessage(
                    peerId=self.group_id, text="Этот предмет не существует"
                )
        else:
            return

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
        item = await price_database.get_item_price(item.capitalize())
        if item:
            price = item["average_price"] * n
            if user["score"] < price:
                response = answers["not enough"].format(score=user["score"])
                await self.api.sendMessage(
                    reply_to=message.messageId, text=response, peerId=self.group_id
                )
            else:
                user["score"] -= price
                await self.database.decrease_score(user_id=user["id"], score=price)

                response = answers["decrease"].format(
                    decrease_score=price, score=user["score"]
                )
                await self.api.sendMessage(
                    reply_to=message.messageId, text=response, peerId=self.group_id
                )
                take_response = f"Взять {item['name']} - {n} штук"
                await self.api.sendMessage(text=take_response, peerId=self.group_id)
                trade_response = f"Передать {item['name']} - {n}"
                await self.api.sendMessage(
                    text=trade_response,
                    peerId=self.group_id,
                    reply_to=message.messageId,
                )
        else:
            await self.api.sendMessage(
                peerId=self.group_id, text="Этот предмет не существует"
            )

    async def balance(self, message: Message, groups: dict):
        user = await self.database.check_user(message.peerId)
        if not user:
            await self.create_user(message.peerId)
            user = await self.database.check_user(message.peerId)

        response = answers["balance"].format(
            score=user["score"],
        )
        await self.api.sendMessage(
            reply_to=message.messageId, text=response, peerId=self.group_id
        )

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
