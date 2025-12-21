from fastapi import FastAPI
from app.routes.car import router as cars_router
from app.routes.sale import router as sales_router
from app.routes.user import router as users_router
from app.routes.customer import router as customers_router
from app.routes.auth import router as auth_router


app = FastAPI(title="API автосалона / API dealership")

app.include_router(cars_router, prefix="/cars", tags=["cars"])
app.include_router(sales_router, prefix="/sales", tags=["sales"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(customers_router, prefix="/customers", tags=["customers"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])