# app/dao/base_dao.py  (или где ты его планируешь хранить)

from sqlalchemy import select
from app.SAmodels.database import async_session_maker


class BaseDAO:
    """
    Базовый DAO для всех моделей.
    В наследниках обязательно нужно указать атрибут model = YourModel
    """
    model = None  

    @classmethod
    async def find_all(cls, **filters):
        """
        Возвращает все записи модели с применением простых фильтров (filter_by).
        Пример: await CarDAO.find_all(brand="Toyota", year=2023)
        """
        async with async_session_maker() as session:
            query = select(cls.model)
            if filters:
                query = query.filter_by(**filters)
            result = await session.execute(query)
            return result.scalars().all()