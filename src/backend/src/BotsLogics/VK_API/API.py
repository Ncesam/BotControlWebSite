import logging
import os
from datetime import datetime
import random
from typing import List, Optional
import aiohttp
from src.BotsLogics.VK_API.Schema import Conversation, Group, Message, User
from src.BotsLogics.VK_API.Schema.File import File
from src.BotsLogics.VK_API.Schema.Group import Chat
from src.BotsLogics.VK_API.Schema.Message import ReplyMessage


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

    async def getTS(self):
        jsonData = await self.__execute("messages.getLongPollServer")
        return jsonData["response"]["ts"]

    async def getMe(self):
        jsonData = await self.__execute("users.get")
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
        self, peerId: int, count: int = 10, offset: int = 0, last_message_id: int = 0
    ) -> List[Message]:
        jsonData = await self.__execute(
            "messages.getHistory",
            count=count,
            offset=offset,
            peer_id=peerId,
            start_message_id=last_message_id,
        )
        resultList = []
        for messageData in jsonData["response"]["items"]:
            message = Message(
                date=datetime.fromtimestamp(messageData["date"]),
                peerId=messageData["from_id"],
                messageId=messageData["id"],
                reply=(
                    ReplyMessage(
                        peerId=messageData["reply_message"]["from_id"],
                        messageId=messageData["reply_message"]["id"],
                        text=messageData["reply_message"]["text"],
                    )
                    if messageData.get("reply_message", None)
                    else None
                ),
                text=messageData["text"],
            )
            resultList.append(message)
        return resultList

    async def sendMessage(
        self,
        peerId: int,
        text: Optional[str] = None,
        reply_to: Optional[int] = None,
        attachment: Optional[str] = None,
    ) -> dict:
        params = {"peer_id": peerId, "random_id": random.randint(100000, 999999)}

        if text is not None:
            params["message"] = text
        if reply_to is not None:
            params["reply_to"] = reply_to
        if attachment is not None:
            params["attachment"] = attachment

        messageId = await self.__execute("messages.send", **params)
        return messageId

    async def uploadFile(self, peerId: int, filename: str):
        uploadUrl = await self.__execute(
            "photos.getMessagesUploadServer", peer_id=peerId
        )
        self.logger.debug(uploadUrl)
        async with aiohttp.ClientSession() as session:
            with open(filename, "rb") as file:
                form = aiohttp.FormData()
                form.add_field(
                    "photo",
                    file,
                    filename=os.path.basename(filename),
                    content_type="image/jpeg",
                )

                response = await session.post(
                    uploadUrl["response"]["upload_url"], data=form
                )
                response.raise_for_status()
                save_params = await response.json()
        file_data = await self.__execute(
            "photos.saveMessagesPhoto",
            photo=save_params["photo"],
            server=save_params["server"],
            hash=save_params["hash"],
        )
        file = File(
            owner_id=file_data["response"][0]["owner_id"],
            photo_id=file_data["response"][0]["id"],
        )
        return file

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
