
from fastapi import APIRouter, Query
from typing import Annotated, List
from app.DAO import SaleDAO
from app.schemas.sale import SaleOut, SaleFilter

router = APIRouter()  

@router.get("", response_model=List[SaleOut], status_code=200, description="Возвращает всю информацию о продажах, обрабатывая все query параметры", summary="Получить информацию о всех продажах")
async def get_sales(
    sale_filter: Annotated[SaleFilter, Query()]
):
    filters = sale_filter.model_dump(exclude_unset=True)
    sales = await SaleDAO.find_all(**filters)
    return sales