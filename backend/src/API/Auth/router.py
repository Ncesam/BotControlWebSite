from fastapi import APIRouter, Depends
from fastapi.responses import Response
from starlette import status
from starlette.requests import Request

from src.API.Auth.logics import AuthLogics

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response, token: tuple[str, str] = Depends(AuthLogics.login_user)
):
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {token[0]}",
        httponly=True,
        max_age=3600,
    )
    response.set_cookie(key="rt", value=f"{token[1]}", httponly=True)
    return {
        "message": "Login Successfully",
        "status": status.HTTP_200_OK,
    }


@router.post("/register", status_code=status.HTTP_200_OK)
async def register(
    response: Response, token: tuple[str, str] = Depends(AuthLogics.register_user)
):
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {token[0]}",
        httponly=True,
        max_age=3600,
    )
    response.set_cookie(key="rt", value=f"{token[1]}", httponly=True)
    return {
        "message": "Register Successfully",
        "status": status.HTTP_200_OK,
    }


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(request: Request, response: Response):
    await AuthLogics.logout_user(request, response)
    return {"message": "Logout Successfully", "status": status.HTTP_200_OK}


@router.get("/me", status_code=status.HTTP_200_OK)
async def me(
    response: Response, user_data: tuple[str, str, str] = Depends(AuthLogics.me)
):
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {user_data[1]}",
        httponly=True,
        max_age=1800,
    )
    response.set_cookie(key="rt", value=f"{user_data[2]}", httponly=True)
    return {
        "status": 200,
        "result": {
            "email": user_data[0],
        },
    }


@router.put("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    response: Response, token: tuple[str, str] = Depends(AuthLogics.refresh_jwt)
):
    response.set_cookie(
        key="Authorization",
        value=f"Bearer {token[0]}",
        httponly=True,
        max_age=1800,
    )
    response.set_cookie(key="rt", value=f"{token[1]}", httponly=True)
    return {
        "message": "Refresh Successfully",
        "status": status.HTTP_200_OK,
    }
