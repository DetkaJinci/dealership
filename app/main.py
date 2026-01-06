import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from redis.asyncio import from_url as async_from_url
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.routes.car import router as cars_router
from app.routes.sale import router as sales_router
from app.routes.user import router as users_router
from app.routes.customer import router as customers_router
from app.routes.auth import router as auth_router

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_url = os.getenv("REDIS_URL")
    redis = async_from_url(
        redis_url,
        encoding="utf-8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="dealership-cache")
    yield
    await redis.close()

app = FastAPI(
    title="API автосалона / Dealership API",
    description="Внутреннее API для управления автомобилями, продажами, пользователями и клиентами",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(cars_router, prefix="/cars", tags=["cars"])
app.include_router(sales_router, prefix="/sales", tags=["sales"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(customers_router, prefix="/customers", tags=["customers"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

