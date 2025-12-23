
from fastapi import APIRouter, HTTPException, Path, Query
from typing import Annotated, List
from app.DAO import CarDAO
from app.schemas.car import CarOut, CarFilter, CarCreate, CarUpdate

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

@router.patch(
    "/{car_id}",
    response_model=CarOut,
    summary="Частично обновить автомобиль",
    description="Обновляет отдельные поля автомобиля по ID. Доступно администраторам и менеджерам."
)
async def update_car(
    car_id: int = Path(..., ge=1, description="ID автомобиля"),
    update_data: CarUpdate = None,
):
    car = await CarDAO.find_one_or_none(id=car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Автомобиль не найден")

    update_values = update_data.model_dump(exclude_unset=True)
    if not update_values:
        return car  

    updated_car = await CarDAO.update(car, **update_values)
    return updated_car


@router.delete(
    "/{car_id}",
    status_code=204,
    summary="Удалить автомобиль",
    description="Полностью удаляет автомобиль из каталога по ID. Доступно только администраторам."
)
async def delete_car(
    car_id: int = Path(..., ge=1, description="ID автомобиля"),
):
    car = await CarDAO.find_one_or_none(id=car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Автомобиль не найден")

    await CarDAO.delete(car)
    return None  
    
