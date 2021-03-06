import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

user = os.getenv("POSTGRES_USER") or "test"
password = os.getenv("POSTGRES_PASSWORD") or "password"
host = os.getenv("POSTGRES_URL") or "localhost"
port = os.getenv("POSTGRES_PORT") or 5432
database = os.getenv("POSTGRES_DATABASE") or "books"

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()