
from fastapi import APIRouter, Query
from typing import Annotated, List
from app.DAO import CarDAO
from app.schemas.car import CarOut, CarFilter

router = APIRouter()  

@router.get("", response_model=List[CarOut])
async def get_cars(
    car_filter: Annotated[CarFilter, Query()]
):
    filters = car_filter.model_dump(exclude_unset=True)
    sales = await CarDAO.find_all(**filters)
    return sales