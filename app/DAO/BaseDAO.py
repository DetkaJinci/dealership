# app/DAO/base_dao.py
from sqlite3 import IntegrityError
from typing import Any, Optional, Sequence
from fastapi import HTTPException, status
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError as SAIntegrityError
from app.SAmodels.database import async_session_maker

# Прямой хэшер Argon2 — безопасный, современный, без лимита длины пароля
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
    Хэширование паролей — через Argon2 (без passlib и bcrypt).
    """
    model = None

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """
        Хэширует пароль с помощью Argon2.
        """
        return ph.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Проверяет пароль против хэша.
        """
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
        Если передан 'password' — автоматически хэширует в 'hashed_password'.
        """
        if "password" in values:
            values["hashed_password"] = cls.get_password_hash(values.pop("password"))

        async with async_session_maker() as session:
            query = insert(cls.model).values(**values).returning(cls.model)
            try:
                result = await session.execute(query)
                await session.commit()
                return result.scalar_one()
            except (IntegrityError, SAIntegrityError) as e:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Нарушение целостности данных (например, дубликат email/username)"
                ) from e

    @classmethod
    async def update(cls, obj: Any, **values) -> Any:
        """
        Обновляет объект.
        Если передан 'password' — хэширует его.
        """
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")

        if "password" in values:
            values["hashed_password"] = cls.get_password_hash(values.pop("password"))

        for key, value in values.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Поле '{key}' не существует в модели {cls.model.__name__}"
                )

        async with async_session_maker() as session:
            session.add(obj)
            try:
                await session.commit()
                await session.refresh(obj)
                return obj
            except (IntegrityError, SAIntegrityError) as e:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Нарушение целостности данных (например, дубликат уникального поля)"
                ) from e

    @classmethod
    async def delete(cls, obj: Any) -> None:
        """
        Удаляет объект.
        """
        if not obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Объект не найден")

        async with async_session_maker() as session:
            session.add(obj)
            await session.delete(obj)
            try:
                await session.commit()
            except (IntegrityError, SAIntegrityError) as e:
                await session.rollback()
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Нельзя удалить: объект связан с другими записями"
                ) from e