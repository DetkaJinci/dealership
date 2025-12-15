from sqlalchemy import Column, Integer, String, Date, DateTime
from app.SAmodels.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    lastname = Column(String(50))  
    birthday = Column(Date)        
    email = Column(String(255), nullable=False) 
    phone = Column(String(20))
    passport = Column(String(50))
