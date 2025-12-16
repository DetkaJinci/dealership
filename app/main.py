from fastapi import FastAPI
from app.routes.car import router as cars_router
from app.routes.sale import router as sales_router

app = FastAPI(title="API автосалона / API dealership")

app.include_router(cars_router, prefix="/cars", tags=["cars"])
app.include_router(sales_router, prefix="/sales", tags=["sales"])