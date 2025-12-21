from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class UserRegister(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: Annotated[str, Field(min_length=8, max_length=128)] = Field(
        ...,
        example="StrongPassword123!",
        description="Пароль должен содержать минимум 8 символов"
    )
    