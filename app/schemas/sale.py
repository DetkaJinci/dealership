from typing import Optional, Literal
from datetime import date, datetime
from pydantic import BaseModel, Field, validator
from decimal import Decimal

class SaleBase(BaseModel):
    car_id: int = Field(gt=0, description="ID автомобиля")
    customer_id: int = Field(gt=0, description="ID покупателя")
    user_id: int = Field(gt=0, description="ID сотрудника (продавца)")
    sale_date: date = Field(description="Дата продажи", example="2024-01-15")
    payment_method: Literal["cash", "card", "credit", "installment"] = Field(
        description="Способ оплаты",
        example="card"
    )
    status: Literal["pending", "completed", "cancelled", "refunded"] = Field(default="completed",
        description="Статус продажи",
        example="completed"
    )
    sale_price: Decimal = Field(
        gt=0, 
        max_digits=12, 
        decimal_places=2,
        description="Цена продажи",
        example=1500000.00
    )


class SaleCreate(SaleBase):
    pass


class SaleUpdate(BaseModel):
    car_id: Optional[int] = Field(None, gt=0, description="ID автомобиля")
    customer_id: Optional[int] = Field(None, gt=0, description="ID покупателя")
    user_id: Optional[int] = Field(None, gt=0, description="ID сотрудника (продавца)")
    sale_date: Optional[date] = Field(None, description="Дата продажи", example="2024-01-15")
    payment_method: Optional[Literal["cash", "card", "credit", "installment"]] = Field(
        None, 
        description="Способ оплаты",
        example="card"
    )
    status: Optional[Literal["pending", "completed", "cancelled", "refunded"]] = Field(
        None,
        description="Статус продажи",
        example="completed"
    )
    sale_price: Optional[Decimal] = Field(
        None,
        gt=0, 
        max_digits=12, 
        decimal_places=2,
        description="Цена продажи",
        example=1500000.00
    )


class SaleOut(SaleBase):
    id: int = Field(description="ID продажи")
    
    class Config:
        from_attributes = True

class SaleFilter(BaseModel):
    """Схема для фильтрации продаж (query parameters)"""
    car_id: Optional[int] = Field(None, gt=0, description="ID автомобиля")
    customer_id: Optional[int] = Field(None, gt=0, description="ID покупателя")
    user_id: Optional[int] = Field(None, gt=0, description="ID сотрудника (продавца)")
    sale_date: Optional[date] = Field(None, description="Дата продажи")
    payment_method: Optional[Literal["cash", "card", "credit", "installment"]] = Field(
        None, description="Способ оплаты"
    )
    status: Optional[Literal["pending", "completed", "cancelled", "refunded"]] = Field(
        None, description="Статус продажи"
    )
