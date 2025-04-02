import asyncio
import logging
import sys

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.API.Auth.router import router as auth_router
from src.API.Bots.router import router as bot_router
from src.API.Config import config
from src.API.Users.router import router as user_router
from src.Controller.main import ControlPanel

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s  %(name)s : %(levelname)s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/logs.log"),
    ],
)

app = FastAPI(version=config.VERSION, docs_url="/docs")

app.include_router(auth_router)

app.include_router(user_router)

app.include_router(bot_router)

app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=5)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_middleware(HTTPSRedirectMiddleware)


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

ControlPanel.start()
