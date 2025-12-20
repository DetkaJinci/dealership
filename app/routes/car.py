from fastapi import APIRouter, Depends
from sqlalchemy import select
from typing import List

from app.SAmodels.database import async_session_maker
from app.SAmodels.car import Car  
from app.schemas.car import CarOut, CarFilter

router = APIRouter()

@router.get("", response_model=List[CarOut])  
async def get_sales(
car_filter: CarFilter = Depends()
):
    async with async_session_maker() as session:
        q = select(Car)
        if car_filter.brand:
            q = q.where(Car.brand == car_filter.brand)        
        result = await session.execute(q)
        cars = result.scalars().all()

        return cars  

