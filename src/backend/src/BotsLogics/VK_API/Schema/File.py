from pydantic import BaseModel


class File(BaseModel):
    owner_id: int
    photo_id: int
