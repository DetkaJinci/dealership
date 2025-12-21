from app.SAmodels.car import Car
from app.SAmodels.customer import Customer
from app.SAmodels.sale import Sale
from app.SAmodels.user import User

from app.DAO.BaseDAO import BaseDAO


class CarDAO(BaseDAO):
    model = Car


class CustomerDAO(BaseDAO):
    model = Customer


class SaleDAO(BaseDAO):
    model = Sale


class UserDAO(BaseDAO):
    model = User

