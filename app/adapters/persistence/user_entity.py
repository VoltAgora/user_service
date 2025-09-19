from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import SmallInteger
from zoneinfo import ZoneInfo
import datetime

Base = declarative_base()

bogota_tz = ZoneInfo("America/Bogota")

def bogota_now():
    return datetime.now(bogota_tz)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    lastname = Column(String(100), nullable=False)
    phone = Column(String(15), nullable=True)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), default=bogota_now)
    is_active = Column(Boolean, default=True)
    role = Column(SmallInteger, nullable=False, default=1)