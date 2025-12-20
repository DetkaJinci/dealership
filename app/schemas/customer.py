from datetime import date
from typing import Literal, Optional
from pydantic import BaseModel, Field, EmailStr

class CustomerBase(BaseModel):
    name: str = Field(min_length=3, max_length=25, description="Имя покупателя", example="Михаил")
    surname: str = Field(min_length=3, max_length=25, description="Фамилия покупателя", example="Моисеев")
    lastname: Optional[str] = Field(min_length=6, max_length=25, description="Отчество покупателя", example="Дмитриевич") 
    birthday: date = Field(description="Дата рождения (ГГГГ-ММ-ДД)", example="2007-05-15")
    email: EmailStr = Field(description="Почта покупателя", example = "biv1s@gmail.com")
    phone: str = Field(min_length=11, max_length=12, description="Номер телефона", example="+79991234567")
    passport: str = Field(min_length=10, max_length=12, description="Серия и номер паспорта", example="1234567890")

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=25, description="Имя покупателя", example="Михаил")
    surname: Optional[str] = Field(min_length=3, max_length=25, description="Фамилия покупателя", example="Моисеев")
    lastname: Optional[str] = Field(min_length=6, max_length=25, description="Отчество покупателя", example="Дмитриевич") 
    birthday: Optional[date] = Field(description="Дата рождения (ГГГГ-ММ-ДД)", example="2007-05-15")
    email: Optional[EmailStr] = Field(description="Почта покупателя", example = "biv1s@gmail.com")
    phone: Optional[str] = Field(min_length=11, max_length=12, description="Номер телефона", example="+79991234567")
    passport: Optional[str] = Field(min_length=10, max_length=12, description="Серия и номер паспорта", example="1234567890")


class CustomerOut(CustomerBase):
    id: int = Field(description="ID записи")


class CustomerFilter(BaseModel):
    """Схема для фильтрации покупателей (query parameters)"""
    name: Optional[str] = Field(None, min_length=3, max_length=25, description="Имя покупателя")
    surname: Optional[str] = Field(None, min_length=3, max_length=25, description="Фамилия покупателя")
    lastname: Optional[str] = Field(None, min_length=6, max_length=25, description="Отчество покупателя")
    birthday: Optional[date] = Field(None, description="Дата рождения")
    email: Optional[EmailStr] = Field(None, description="Почта покупателя")
    phone: Optional[str] = Field(None, min_length=11, max_length=12, description="Номер телефона")
    passport: Optional[str] = Field(None, min_length=10, max_length=12, description="Паспорт")

