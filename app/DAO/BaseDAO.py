from sqlite3 import IntegrityError
from typing import Optional, Sequence
from fastapi import HTTPException
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError as SAIntegrityError
from app.SAmodels.database import async_session_maker
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class BaseDAO:
    """
    Базовый DAO для всех моделей.
    """
    model = None

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """
        Для хэширования пароля.
        используется при создании/обновлении пользователя.
        """
        return pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        """
        Проверка пароля.
        """
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    async def find_one_or_none(cls, **filters) -> Optional[model]:
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filters) -> Sequence[model]:
        async with async_session_maker() as session:
            query = select(cls.model)
            if filters:
                query = query.filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **values):
        """
        Метод для создания.
        ДЛЯ ЮЗЕРА хэширует поле hashed_password.
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
                    status_code=400,
                    detail="Database integrity error (e.g. duplicate email/username)"
                ) from e