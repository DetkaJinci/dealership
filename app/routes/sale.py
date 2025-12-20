from fastapi import APIRouter, Depends
from sqlalchemy import select
from typing import List

from app.SAmodels.database import async_session_maker
from app.SAmodels.sale import Sale  
from app.schemas.sale import SaleOut, SaleFilter

router = APIRouter()


@router.get("", response_model=List[SaleOut])  
async def get_sales(
sale_filter: SaleFilter = Depends()
):
    async with async_session_maker() as session:
        q = select(Sale)
        if sale_filter.car_id:
            q = q.where(Sale.car_id == sale_filter.car_id)        
        result = await session.execute(q)
        sales = result.scalars().all()

        if sale_filter.user_id:
            q = q.where(Sale.user_id == sale_filter.user_id)
        return sales  


            