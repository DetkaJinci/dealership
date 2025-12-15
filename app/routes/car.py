from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.SAmodels.car import Car as SAModelCar
from app.schemas.car import CarBase, CarCreate, CarUpdate, CarOut
from app.SAmodels.database import get_db  

router = APIRouter()

@router.get("/", response_model=CarOut)
def get_cars():
    return "поршик панамера"