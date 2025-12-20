from decimal import Decimal
from typing import Literal, Optional
from pydantic import BaseModel, Field

from typing import Optional, Literal
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, validator
import re


class UserBase(BaseModel):
    username: str = Field(
        min_length=3, 
        max_length=50, 
        description="Логин пользователя", 
        example="ivanov"
    )
    birthday: date = Field(
        description="Дата рождения пользователя", 
        example="1990-05-15"
    )
    email: EmailStr = Field(
        description="Email пользователя", 
        example="ivanov@example.com"
    )
    role: Literal["admin", "manager", "seller", "viewer"] = Field(
        description="Роль пользователя в системе",
        example="seller"
    )
    


class UserCreate(UserBase):
    password: str = Field(
        min_length=8, 
        max_length=100, 
        description="Пароль пользователя",
        example="StrongPass123!"
    )
    


class UserUpdate(BaseModel):
    username: Optional[str] = Field(
        None, 
        min_length=3, 
        max_length=50, 
        description="Логин пользователя", 
        example="ivanov"
    )
    birthday: Optional[date] = Field(
        None, 
        description="Дата рождения пользователя", 
        example="1990-05-15"
    )
    email: Optional[EmailStr] = Field(
        None, 
        description="Email пользователя", 
        example="ivanov@example.com"
    )
    role: Optional[Literal["admin", "manager", "seller", "viewer"]] = Field(
        None, 
        description="Роль пользователя в системе",
        example="seller"
    )
    password: Optional[str] = Field(
        None,
        min_length=8, 
        max_length=100, 
        description="Пароль пользователя",
        example="NewStrongPass123!"
    )
    


class UserOut(UserBase):
    id: int = Field(description="ID пользователя")



class UserOutWithoutSensitive(UserOut):
    """Версия UserOut без даты рождения для публичных данных"""
    birthday: Optional[date] = Field(None, description="Дата рождения (скрыта для безопасности)")
    
    class Config:
        from_attributes = True


class UserFilter(BaseModel):
    """Схема для фильтрации пользователей (query parameters)"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Логин пользователя")
    birthday: Optional[date] = Field(None, description="Дата рождения")
    email: Optional[EmailStr] = Field(None, description="Email пользователя")
    role: Optional[Literal["admin", "manager", "seller", "viewer"]] = Field(
        None, description="Роль пользователя в системе"
    )

