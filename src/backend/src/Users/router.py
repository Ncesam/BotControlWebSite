from fastapi import APIRouter, Depends

from src.Users.logics import UsersLogics

router = APIRouter(prefix="/api/user", tags=["User"])


@router.post("")
async def get_user(result: dict = Depends(UsersLogics.get_users)):
    response = {
        "status": 200,
        "result": result,
    }
    return response
