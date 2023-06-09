from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
# SQLALCHEMY_DATABASE_URL = 'postgresql://swetanshudubey:Sekhar123@localhost:5432/fastapi_db'
print(f'postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}:@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}')
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}:@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
print({"Engin Error : " : engine})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    print({"Databse Info : ": db})
    try:
        yield db
    finally:
        db.close()