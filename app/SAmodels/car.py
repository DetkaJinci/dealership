from sqlalchemy import Column, Integer, String
from app.SAmodels.database import Base 


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), index=True, nullable=False)
    model = Column(String(100), index=True, nullable=False)
    year = Column(Integer, nullable=False, index=True)
    color = Column(String(30), nullable=False)
    status = Column(String(20), nullable=False, index=True)  
    price = Column(Integer, nullable=False)

