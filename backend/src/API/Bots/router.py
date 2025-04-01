from fastapi import APIRouter
from fastapi import Depends
from starlette import status

from src.API.Bots.exceptions import BotUpdateError
from src.API.Bots.logics import BotsLogics

router = APIRouter(prefix="/api/bots", tags=["Bots"])


@router.get("")
async def get_bots(bots=Depends(BotsLogics.get_bots)):
    if bots:
        return {"status": 200, "result": bots}
    return {
        "status": status.HTTP_204_NO_CONTENT,
        "message": "User doesn't have any bots",
    }


@router.post("")
async def add_bot(bot=Depends(BotsLogics.add_bot)):
    return {"status": status.HTTP_201_CREATED, "message": "Bot added"}


@router.put("/start")
async def start_bot(bots=Depends(BotsLogics.start_bots)):
    return {"status": status.HTTP_200_OK, "result": bots}


@router.delete("")
async def delete_bot(bot=Depends(BotsLogics.delete_bot)):
    return {"status": status.HTTP_200_OK, "message": bot}


@router.put("/stop")
async def stop_bot(bots=Depends(BotsLogics.stop_bots)):
    return {"status": status.HTTP_200_OK, "result": bots}


@router.put("")
async def update_bot(bot=Depends(BotsLogics.update_bot)):
    if not bot:
        raise BotUpdateError
    return {"status": status.HTTP_200_OK, "message": bot}
