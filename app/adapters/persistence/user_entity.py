from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document = Column(String(50), unique=True, nullable=False)
    name = Column(String(100))
    lastname = Column(String(100))
    phone = Column(String(20))
    email = Column(String(200), unique=True)
    created_at = Column(DateTime)
    is_active = Column(Boolean, default=True)