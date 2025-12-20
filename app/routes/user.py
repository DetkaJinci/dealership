from fastapi import APIRouter, Depends
from sqlalchemy import select
from typing import List

from app.SAmodels.database import async_session_maker
from app.SAmodels.user import User  
from app.schemas.user import UserOut, UserFilter


router = APIRouter()


router.get("", response_model=List[UserOut])
async def get_users(user_filter: UserFilter = Depends()):
    with async_session_maker() as session:
        q = select(User)
        
        result = await session.execute(q)
        users = result.scalars().all()
        return users
