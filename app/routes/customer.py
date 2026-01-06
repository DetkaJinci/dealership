from fastapi import APIRouter, HTTPException, Path, Query
from typing import Annotated, List
from app.DAO import CustomerDAO
from app.schemas.customer import CustomerOut, CustomerFilter, CustomerCreate, CustomerUpdate
from fastapi_cache.decorator import cache

router = APIRouter()  

@router.get("", response_model=List[CustomerOut], status_code=200, description="Возвращает всех покупателей, обрабатывая все query параметры", summary="Получить всех покупателей")
@cache(expire=60)
async def get_customers(
    customer_filter: Annotated[CustomerFilter, Query()]
):
    filters = customer_filter.model_dump(exclude_unset=True)
    sales = await CustomerDAO.find_all(**filters)
    return sales

@router.post(
    "",
    response_model=CustomerOut,
    status_code=201,
    summary="Создать нового покупателя",
    description="Добавляет нового покупателя в систему. Доступно администраторам и менеджерам."
)
async def create_customer(values: CustomerCreate):
    customer_data = values.model_dump()
    new_customer = await CustomerDAO.add(**customer_data)
    return new_customer


@router.patch(
    "/{customer_id}",
    response_model=CustomerOut,
    summary="Частично обновить покупателя",
    description="Обновляет отдельные поля покупателя по ID. Доступно администраторам и менеджерам."
)
async def update_customer(
    customer_id: int = Path(..., ge=1, description="ID покупателя"),
    update_data: CustomerUpdate = None,
):
    customer = await CustomerDAO.find_one_or_none(id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Покупатель не найден")

    update_values = update_data.model_dump(exclude_unset=True)
    if not update_values:
        return customer  

    updated_customer = await CustomerDAO.update(customer, **update_values)
    return updated_customer

@router.delete(
    "/{customer_id}",
    status_code=204,
    summary="Удалить покупателя",
    description="Полностью удаляет покупателя по ID. Доступно только администраторам."
)
async def delete_customer(
    customer_id: int = Path(..., ge=1, description="ID покупателя"),
):
    customer = await CustomerDAO.find_one_or_none(id=customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Покупатель не найден")

    await CustomerDAO.delete(customer)
    return None  