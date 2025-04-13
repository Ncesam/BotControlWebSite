import logging
import multiprocessing
import os

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.cors import CORSMiddleware

from src.Auth.router import router as auth_router
from src.Bots.router import router as bot_router
from src.BotsLogics.ControlPanel import ControlPanel
from src.BotsLogics.PriceChecker import price_updater_start
from src.Config import config
from src.Users.router import router as user_router

if not os.path.exists("logs/"):
    os.mkdir("logs")
if not os.path.exists("logs/logs.log"):
    with open("logs/logs.log", "w") as f:
        pass

logging.basicConfig(
    level=logging.INFO,
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

origins = ["http://localhost", "http://localhost:8080", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.add_middleware(HTTPSRedirectMiddleware)


@app.on_event("startup")
async def startup():
    # loop.create_task(price_database.add_all_item())
    multiprocessing.Process(target=price_updater_start).start()
    ControlPanel.start()
