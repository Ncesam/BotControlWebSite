import logging
from datetime import datetime
import random
from typing import List
import aiohttp
from src.VK_API.Schema import Conversation, Group, Message, User
from src.VK_API.Schema.Group import Chat


class APIError(Exception):
    def __init__(self, msg):
        self.msg = msg


class API:
    baseUrl = "https://api.vk.com/method/"
    logger = logging.getLogger(__name__)

    def __init__(self, accessToken: str):
        self.accessToken = accessToken

    async def __execute(self, method: str, **paramsToAdd) -> str:
        async with aiohttp.ClientSession() as session:
            params = {"access_token": self.accessToken, "v": 5.199, **paramsToAdd}

            response = await session.get(self.baseUrl + method, params=params)
            response.raise_for_status()
            jsonData = await response.json()
            response.close()
            if jsonData.get("error"):
                raise APIError(jsonData)
            return jsonData

    async def getUser(self, userId: int) -> User:
        jsonData = await self.__execute("users.get", user_ids=userId)
        user = User(
            firstName=jsonData["response"][0]["first_name"],
            lastName=jsonData["response"][0]["last_name"],
            userId=jsonData["response"][0]["id"],
        )
        return user

    async def getConversations(self, offset: int = 0) -> List[Conversation]:
        jsonData = await self.__execute("messages.getConversations", offset=offset)
        resultList = []
        for conversationData in jsonData["response"]["items"]:
            conversation = Conversation(
                conversationType=conversationData["conversation"]["peer"]["type"],
                peerId=conversationData["conversation"]["peer"]["id"],
                textLastMessage=conversationData["last_message"]["text"],
            )
            resultList.append(conversation)
        return resultList

    async def getHistoryMessages(
        self, peerId: int, count: int = 10, offset: int = 0
    ) -> List[Message]:
        jsonData = await self.__execute(
            "messages.getHistory", count=count, offset=offset, peer_id=peerId
        )
        resultList = []
        for messageData in jsonData["response"]["items"]:
            message = Message(
                date=datetime.fromtimestamp(messageData["date"]),
                peerId=messageData["from_id"],
                messageId=messageData["id"],
                text=messageData["text"],
            )
            resultList.append(message)
        return resultList

    async def sendMessage(self, peerId: int, reply_to: int, text: str) -> dict:
        messageId = await self.__execute(
            "messages.send",
            peer_id=peerId,
            message=text,
            reply_to=reply_to,
            random_id=random.randint(100000, 999999),
        )
        return messageId

    async def getGroup(self, peerId: int) -> Group:
        jsonData = await self.__execute("groups.getById", group_id=abs(peerId))
        group = Group(
            peerId=jsonData["response"]["groups"][0]["id"],
            name=jsonData["response"]["groups"][0]["name"],
        )
        return group

    async def getChat(self, peerId: int) -> Chat:
        jsonData = await self.__execute("messages.getChat", chat_id=peerId - 2000000000)
        self.logger.debug(jsonData)
        chat = Chat(
            peerId=jsonData["response"]["id"], name=jsonData["response"]["title"]
        )
        return chat
