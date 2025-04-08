from sqlalchemy import ForeignKey, String, ARRAY
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.API.DataBase import Base


class Bot(Base):
    __tablename__ = "Bot"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"), nullable=False)
    token: Mapped[str]
    group_name: Mapped[str]
    answers_type: Mapped[str] = mapped_column(default="storage")
    nicknames: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    text: Mapped[str] = mapped_column(nullable=True)

    user: Mapped["User"] = relationship(back_populates="bots")
