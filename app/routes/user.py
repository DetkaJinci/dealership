
from fastapi import APIRouter, Query
from typing import Annotated, List
from app.DAO import UserDAO
from app.schemas.user import UserOut, UserFilter

router = APIRouter()  

@router.get("", response_model=List[UserOut], status_code=200, description="Возвращает всех пользователей, обрабатывая все query параметры", summary="Получить всех пользователей")
async def get_users(
    user_filter: Annotated[UserFilter, Query()]
):
    filters = user_filter.model_dump(exclude_unset=True)
    sales = await UserDAO.find_all(**filters)
    return sales