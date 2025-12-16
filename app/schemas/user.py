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
    


class UserOut(BaseModel):
    id: int = Field(description="ID пользователя")
    username: str = Field(description="Логин пользователя", example="ivanov")
    birthday: date = Field(description="Дата рождения пользователя", example="1990-05-15")
    email: str = Field(description="Email пользователя", example="ivanov@example.com")
    role: str = Field(description="Роль пользователя", example="seller")
    created_at: datetime = Field(description="Дата создания пользователя")
    updated_at: Optional[datetime] = Field(None, description="Дата обновления данных")
    
    class Config:
        from_attributes = True


class UserOutWithoutSensitive(UserOut):
    """Версия UserOut без даты рождения для публичных данных"""
    birthday: Optional[date] = Field(None, description="Дата рождения (скрыта для безопасности)")
    
    class Config:
        from_attributes = True


class SaleFilter(BaseModel):
    """Схема для фильтрации продаж (query parameters)"""
    car_id: Optional[int] = Field(None, gt=0, description="ID автомобиля")
    customer_id: Optional[int] = Field(None, gt=0, description="ID покупателя")
    user_id: Optional[int] = Field(None, gt=0, description="ID сотрудника (продавца)")
    sale_date_from: Optional[date] = Field(None, description="Дата продажи от")
    sale_date_to: Optional[date] = Field(None, description="Дата продажи до")
    payment_method: Optional[Literal["cash", "card", "credit", "installment"]] = Field(
        None, description="Способ оплаты"
    )
    status: Optional[Literal["pending", "completed", "cancelled", "refunded"]] = Field(
        None, description="Статус продажи"
    )
    sale_price_min: Optional[Decimal] = Field(
        None, gt=0, max_digits=12, decimal_places=2, description="Минимальная цена продажи"
    )
    sale_price_max: Optional[Decimal] = Field(
        None, gt=0, max_digits=12, decimal_places=2, description="Максимальная цена продажи"
    )