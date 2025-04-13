from typing import List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.DataBase import Base


class User(Base):
    __tablename__ = "User"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    refresh_token: Mapped[str] = mapped_column(nullable=True)

    bots: Mapped[List["Bot"]] = relationship(back_populates="user")
