from fastapi import APIRouter, Depends
from sqlalchemy import select
from typing import List

from app.SAmodels.database import async_session_maker
from app.SAmodels.customer import Customer  
from app.schemas.customer import CustomerOut, CustomerFilter


router = APIRouter()


@router.get("", response_model=List[CustomerOut])
async def get_customers(
customers_filter: CustomerFilter = Depends()
    ):
    with async_session_maker() as session:
        q = select(Customer)
        result = await session.execute(q)
        customers = result.scalars.all()
        return customers







