from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Index
from sqlalchemy.sql import func
from app.SAmodels.database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"), index=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    sale_date = Column(DateTime, server_default=func.now())
    payment_method = Column(String(50), nullable=False)  
    status = Column(String(20), default="completed")    
    sale_price = Column(Numeric(10, 2), nullable=False)  