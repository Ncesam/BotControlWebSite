import logging
import os
from typing import List, Union

from fastapi import UploadFile


def prepare_nickname_string(nicknames: Union[str, List[str]]) -> List[str]:
    """Корректно обрабатывает никнеймы, независимо от типа входных данных."""
    if isinstance(nicknames, str):
        return [nick.strip() for nick in nicknames.split(",") if nick.strip()]
    elif isinstance(nicknames, list):
        return [nick.strip() for nick in nicknames if isinstance(nick, str)]
    return []


async def upload_file(bot_id: int, file: UploadFile):
    file.filename = f"{bot_id}.{file.filename.split('.')[-1]}"
    filename = os.path.join(os.getcwd(), "images", file.filename)
    if not os.path.exists(os.path.join(os.getcwd(), "images")):
        os.mkdir(os.path.join(os.getcwd(), "images"))
    with open(filename, "wb+") as f:
        logging.debug("Upload File" + " " + filename)
        f.write(await file.read())
        f.close()
