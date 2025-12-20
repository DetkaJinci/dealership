
from fastapi import APIRouter, Query
from typing import Annotated, List
from app.DAO import CustomerDAO
from app.schemas.customer import CustomerOut, CustomerFilter

router = APIRouter()  

@router.get("", response_model=List[CustomerOut])
async def get_customers(
    customer_filter: Annotated[CustomerFilter, Query()]
):
    filters = customer_filter.model_dump(exclude_unset=True)
    sales = await CustomerDAO.find_all(**filters)
    return sales