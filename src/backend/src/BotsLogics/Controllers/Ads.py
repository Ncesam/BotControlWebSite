import asyncio
from src.BotsLogics.Config import config
from src.BotsLogics.BaseController import BaseController


@BaseController.register_controller("ads")
class AdsController(BaseController):
    async def loop(self):
        attachment = None

        filepath = self.find_bot_image(self.bot.id)

        if filepath:
            try:
                file = await self.api.uploadFile(self.group_id, filepath)
                attachment = f"photo{file.owner_id}_{file.photo_id}"
                self.logger.info(
                    f"Файл рекламы для бота {self.bot.id} успешно загружен."
                )
            except Exception as e:
                self.logger.error(
                    f"Не удалось загрузить файл рекламы для бота {self.bot.id}: {e}"
                )
        else:
            self.logger.warning(
                f"Файл рекламы не найден по пути: {filepath}. Будет отправлено без вложения."
            )

        while True:
            try:
                await self.api.sendMessage(
                    peerId=self.group_id,
                    text=self.bot.text,
                    attachment=attachment if attachment else None,
                )
                await asyncio.sleep(config.ADS_DELAY * 60)
            except Exception as e:
                self.logger.error(f"Ошибка в ads loop у бота {self.bot.id}: {e}")
                await asyncio.sleep(60)
