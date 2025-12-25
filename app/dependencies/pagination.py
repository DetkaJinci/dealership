from typing import Optional
from fastapi import Query

class PaginationParams:
    """
    Пагинация
    """
    def __init__(
        self,
        skip: Optional[int] = Query(0, ge=0, description="Сколько записей пропустить"),
        limit: Optional[int] = Query(20, ge=1, le=100, description="Максимальное количество записей на страницу")
    ):
        self.skip = skip
        self.limit = limit