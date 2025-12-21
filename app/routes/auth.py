# app/routes/auth.py (или где у тебя роуты)
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserCreate, UserOut
from app.DAO import UserDAO 

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=201)
async def register_user(user_data: UserCreate):
    # Проверка на существующий email
    if await UserDAO.find_one_or_none(email=user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Проверка на существующий username
    if await UserDAO.find_one_or_none(username=user_data.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = await UserDAO.add(
        username=user_data.username,
        email=user_data.email,
        birthday=user_data.birthday,
        role=user_data.role,
        password=user_data.password, 
    )

    return new_user