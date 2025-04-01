import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy import select, delete, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.orm import DeclarativeBase, joinedload

from src.API.Config import config
from src.API.Exceptions import ServerError, SQLalchemyError


class Base(DeclarativeBase):
    pass


class DataBaseSessionCreator:
    def __init__(self):
        async_engine = create_async_engine(
            url=config.POSTGRES_URL,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800,
        )
        self.maker = async_sessionmaker(
            bind=async_engine, expire_on_commit=False, class_=AsyncSession
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession | Any, Any]:
        async with self.maker() as session:
            yield session


SessionCreator = DataBaseSessionCreator()


class BaseDTO:
    model: Base
    logger: logging.Logger

    @classmethod
    async def select_by_filters(cls, **filters):
        async with SessionCreator.get_session() as session:
            try:
                stmt = select(cls.model).filter_by(**filters)
            except ValueError as e:
                cls.logger.error(f"Failed to select data {e}")
                raise ServerError()
            try:
                result = await session.execute(stmt)
                return result.scalars().all()
            except SQLAlchemyError as e:
                cls.logger.error(f"SQLAlchemy error {e}")
                raise SQLalchemyError

    @classmethod
    async def select_all(cls):
        async with SessionCreator.get_session() as session:
            try:
                stmt = select(cls.model)
            except ValueError as e:
                cls.logger.error(f"Failed to select data {e}")
                raise ServerError()
            try:
                result = await session.execute(stmt)
                return result.scalars().all()
            except SQLAlchemyError as e:
                cls.logger.error(f"SQLAlchemy error {e}")
                raise SQLalchemyError

    @classmethod
    async def select_one_or_none(cls, **filters):
        async with SessionCreator.get_session() as session:
            try:
                stmt = select(cls.model).filter_by(**filters)
            except ValueError as e:
                cls.logger.error(f"Failed to select data {e}")
                raise ServerError()
            try:
                result = await session.execute(stmt)
                return result.scalars().one_or_none()
            except SQLAlchemyError as e:
                cls.logger.error(f"SQLAlchemy error {e}")
                raise SQLalchemyError

    @classmethod
    async def select_with_some(cls, some: str, **filters):
        async with SessionCreator.get_session() as session:
            try:
                stmt = (
                    select(cls.model)
                    .options(joinedload(getattr(cls.model, some)))
                    .filter_by(**filters)
                )
            except ValueError as e:
                cls.logger.error(f"Failed to select data {e}")
                raise ServerError()
            try:
                result = await session.execute(stmt)
                return result.unique().scalars().first()
            except SQLAlchemyError as e:
                cls.logger.error(f"SQLAlchemy error {e}")
                raise SQLalchemyError

    @classmethod
    async def update(cls, new_data: dict, **filters):
        async with SessionCreator.get_session() as session:
            try:
                stmt = update(cls.model).filter_by(**filters).values(**new_data)
            except ValueError as e:
                cls.logger.error(f"Failed to update data {e}")
                raise ServerError
            try:
                await session.execute(stmt)
                await session.commit()
            except SQLAlchemyError as e:
                cls.logger.error(f"SQLAlchemy error {e}")
                raise SQLalchemyError

    @classmethod
    async def insert(cls, model_instance: Base):
        async with SessionCreator.get_session() as session:
            try:
                session.add(model_instance)
                await session.commit()
                return True
            except IntegrityError as e:
                await session.rollback()
                cls.logger.error(f"IntegrityError {e}")
                return None
            except SQLAlchemyError as e:
                await session.rollback()
                cls.logger.error(f"SQLAlchemy error {e}")
                raise SQLalchemyError

    @classmethod
    async def delete_by_filters(cls, **filters):
        async with SessionCreator.get_session() as session:
            try:
                stmt = delete(cls.model).filter_by(**filters)
            except ValueError as e:
                cls.logger.error(f"Failed to delete data {e}")
                raise ServerError()
            try:
                await session.execute(stmt)
                await session.commit()
            except SQLAlchemyError as e:
                cls.logger.error(f"SQLAlchemy error {e}")
                raise SQLalchemyError
