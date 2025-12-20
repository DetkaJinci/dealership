from typing import Literal, Optional
from pydantic import BaseModel, Field

class CarBase(BaseModel):
    brand: str = Field(min_length=1, max_length=50, description="Марка автомобиля", example="Toyota")
    model: str = Field(min_length=1, max_length=100, description="Модель автомобиля", example="Camry")
    year: int = Field(ge=1886, le=2026, description="Год выпуска", example=2023)
    color: str = Field(min_length=3, max_length=30, description="Цвет автомобиля", example="Синий")
    status: Literal["в наличии", "не в наличии", "зарезервировано"] = Field(..., description="Статус автомобиля")
    price: int = Field(gt=0, description="Цена в рублях", example=2500000)


class CarCreate(CarBase):
    """Схема для создания нового автомобиля."""
    pass


class CarUpdate(BaseModel):
    """Схема для частичного обновления автомобиля."""
    brand: Optional[str] = Field(None, min_length=1, max_length=50, description="Марка автомобиля", example="Toyota")
    model: Optional[str] = Field(None, min_length=1, max_length=100, description="Модель автомобиля", example="Camry")
    year: Optional[int] = Field(None, ge=1886, le=2026, description="Год выпуска", example=2023)
    color: Optional[str] = Field(None, min_length=3, max_length=30, description="Цвет автомобиля", example="Синий")
    status: Optional[Literal["в наличии", "не в наличии", "зарезервировано"]] = Field(None, description="Статус автомобиля")
    price: Optional[int] = Field(None, gt=0, description="Цена в рублях", example=2500000.0)

class CarOut(CarBase):
    """Схема для отображения автомобиля в responsive model(в ответе)."""
    id: int = Field(..., description="Уникальный айдишник автомобиля", example=1)

    model_config = {
        "from_attributes": True             
    }    

class CarFilter(BaseModel):
    """Схема для фильтрации автомобилей (query parameters)"""
    brand: Optional[str] = Field(None, min_length=1, max_length=50, description="Марка автомобиля")
    model: Optional[str] = Field(None, min_length=1, max_length=100, description="Модель автомобиля")
    year: Optional[int] = Field(None, ge=1886, le=2026, description="Год выпуска")
    color: Optional[str] = Field(None, min_length=3, max_length=30, description="Цвет автомобиля")
    status: Optional[Literal["в наличии", "не в наличии", "зарезервировано"]] = Field(None, description="Статус автомобиля")

