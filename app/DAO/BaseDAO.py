from sqlite3 import IntegrityError
from typing import Any, Optional, Sequence
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError as SAIntegrityError

from app.SAmodels.database import async_session_maker
from app.exceptions import (  # <-- Импортируем твои кастомные исключения
    UserAlreadyExistsException,
    ObjectNotFoundException,
    IntegrityViolationException,
)

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError

ph = PasswordHasher(
    memory_cost=102400,
    time_cost=3,
    parallelism=2,
)


class BaseDAO:
    """
    Базовый DAO для всех моделей.
    Поддерживает полный CRUD.
    Хэширование паролей — через Argon2.
    Использует кастомные исключения для лучшей читаемости и унификации ошибок.
    """
    model = None

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return ph.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        try:
            ph.verify(hashed_password, plain_password)
            return True
        except (VerifyMismatchError, InvalidHashError):
            return False

    @classmethod
    async def find_one_or_none(cls, **filters) -> Optional[Any]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filters) -> Sequence[Any]:
        async with async_session_maker() as session:
            query = select(cls.model)
            if filters:
                query = query.filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values) -> Any:
        """
        Создаёт новую запись.
        Автоматически хэширует пароль, если передан.
        При дубликате уникального поля (email/username) — кидает UserAlreadyExistsException.
        """
        if "password" in values:
            values["hashed_password"] = cls.get_password_hash(values.pop("password"))

        async with async_session_maker() as session:
            query = insert(cls.model).values(**values).returning(cls.model)
            try:
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one()
            except (IntegrityError, SAIntegrityError):
                await session.rollback()
                raise UserAlreadyExistsException()

    @classmethod
    async def update(cls, obj: Any, **values) -> Any:
        """
        Обновляет существующий объект.
        """
        if not obj:
            raise ObjectNotFoundException(cls.model.__name__)

        if "password" in values:
            values["hashed_password"] = cls.get_password_hash(values.pop("password"))

        for key, value in values.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
            else:
                raise IntegrityViolationException(
                    detail=f"Поле '{key}' не существует в модели {cls.model.__name__}"
                )

        async with async_session_maker() as session:
            session.add(obj)
            try:
                await session.commit()
                await session.refresh(obj)
                return obj
            except (IntegrityError, SAIntegrityError):
                await session.rollback()
                raise IntegrityViolationException(
                    detail="Нарушение целостности данных (например, дубликат уникального поля)"
                )

    @classmethod
    async def delete(cls, obj: Any) -> None:
        """
        Удаляет объект.
        """
        if not obj:
            raise ObjectNotFoundException(cls.model.__name__)

        async with async_session_maker() as session:
            session.add(obj)
            await session.delete(obj)
            try:
                await session.commit()
            except (IntegrityError, SAIntegrityError):
                await session.rollback()
                raise IntegrityViolationException(
                    detail="Нельзя удалить: объект связан с другими записями"
                )