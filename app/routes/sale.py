from fastapi import APIRouter, HTTPException, Path, Query, Depends
from typing import Annotated, List
from app.DAO import SaleDAO
from app.schemas.sale import SaleOut, SaleFilter, SaleCreate, SaleUpdate
from app.dependencies.auth import get_current_user
from app.SAmodels.user import User  
from fastapi_cache.decorator import cache

router = APIRouter()

@router.get(
    "",
    response_model=List[SaleOut],
    status_code=200,
    description="Возвращает всю информацию о продажах, обрабатывая все query параметры",
    summary="Получить информацию о всех продажах",
)
@cache(expire=60)
async def get_sales(
    sale_filter: Annotated[SaleFilter, Query()],
    current_user: User = Depends(get_current_user)  
):
    filters = sale_filter.model_dump(exclude_unset=True)
    sales = await SaleDAO.find_all(**filters)
    return sales


@router.post(
    "",
    response_model=SaleOut,
    status_code=201,
    summary="Создать новую продажу",
    description="Добавляет новую продажу. Только для администраторов и менеджеров."
)
async def create_sale(
    values: SaleCreate,
    current_user: User = Depends(get_current_user)  
):
    sale_data = values.model_dump()
    new_sale = await SaleDAO.add(**sale_data)
    return new_sale


@router.patch(
    "/{sale_id}",
    response_model=SaleOut,
    summary="Частично обновить продажу",
    description="Обновляет отдельные поля продажи по ID. Доступно администраторам и менеджерам."
)
async def update_sale(
    sale_id: int = Path(..., ge=1, description="ID продажи"),
    update_data: SaleUpdate = None,
    current_user: User = Depends(get_current_user)  
):
    sale = await SaleDAO.find_one_or_none(id=sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Продажа не найдена")

    update_values = update_data.model_dump(exclude_unset=True)
    if not update_values:
        return sale  

    updated_sale = await SaleDAO.update(sale, **update_values)
    return updated_sale


@router.delete(
    "/{sale_id}",
    status_code=204,
    summary="Удалить продажу",
    description="Полностью удаляет запись о продаже по ID. Доступно только администраторам."
)
async def delete_sale(
    sale_id: int = Path(..., ge=1, description="ID продажи"),
    current_user: User = Depends(get_current_user)  
):
    sale = await SaleDAO.find_one_or_none(id=sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Продажа не найдена")

    await SaleDAO.delete(sale)
    return None