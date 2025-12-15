from sqlalchemy import Column, Integer, String, Date
from app.SAmodels.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    birthday = Column(Date, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(String(20), nullable=False, default="user")
    hashed_password = Column(String(255), nullable=False)