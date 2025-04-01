from src.API.Bots.service import BotService


class ControllerService:
    @classmethod
    async def get_enabled_bots(cls):
        bots = await BotService.get_bot(status=True)
        return bots
