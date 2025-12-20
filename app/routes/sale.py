
from fastapi import APIRouter, Query
from typing import Annotated, List
from app.DAO import SaleDAO
from app.schemas.sale import SaleOut, SaleFilter

router = APIRouter()  

@router.get("", response_model=List[SaleOut])
async def get_sales(
    sale_filter: Annotated[SaleFilter, Query()]
):
    filters = sale_filter.model_dump(exclude_unset=True)
    sales = await SaleDAO.find_all(**filters)
    return sales