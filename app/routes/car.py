
from fastapi import APIRouter, HTTPException, Query
from typing import Annotated, List
from app.DAO import CarDAO
from app.schemas.car import CarOut, CarFilter, CarCreate

router = APIRouter()  

@router.get("", response_model=List[CarOut], status_code=200, summary="Получить все автомобили", description="Возвращает все автомобили, обрабатывая все query параметры")
async def get_cars(
    car_filter: Annotated[CarFilter, Query()]
):
    filters = car_filter.model_dump(exclude_unset=True)
    cars = await CarDAO.find_all(**filters)
    return cars

@router.post(
    "",
    response_model=CarOut,
    status_code=201,
    summary="Создать новый автомобиль",
    description="Добавляет автомобиль. Только для администраторов и менеджеров."
)
async def create_car(values: CarCreate):
    car_data = values.model_dump()
    new_car = await CarDAO.add(**car_data)
    return new_car

    
