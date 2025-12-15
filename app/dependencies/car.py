from typing import Optional, Literal
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class CarQueryFilters(BaseModel):
    brand: Optional[str] = Field(
        None,
        description="Марка автомобиля",
        min_length=1,
        max_length=50
    )
    model: Optional[str] = Field(
        None,
        description="Модель автомобиля",
        min_length=1,
        max_length=100
    )
    year: Optional[int] = Field(
        None,
        description="Год выпуска",
        ge=1886,
        le=2026
    )
    status: Optional[Literal["в наличии", "нет в наличии", "зарезервировано"]] = Field(
        None,
        description="Статус автомобиля"
    )
    min_price: Optional[int] = Field(
        None,
        description="Минимальная цена",
        ge=1
    )
    max_price: Optional[int] = Field(
        None,
        description="Максимальная цена",
        ge=1
    )