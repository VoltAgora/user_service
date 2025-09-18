import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.adapters.persistence.user_entity import Base

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# helper para crear tablas en dev
def init_db():
    Base.metadata.create_all(bind=engine)