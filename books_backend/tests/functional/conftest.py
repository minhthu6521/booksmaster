import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from app import app
from database import Base
from tests.utils import init_data
from tests.utils import test_book_data

used = test_book_data


@pytest.fixture(scope="function")
def client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="function")
def clean_db(client):
    user = os.getenv("POSTGRES_USER") or "test"
    password = os.getenv("POSTGRES_PASSWORD") or "password"
    host = os.getenv("POSTGRES_URL") or "localhost"
    port = os.getenv("POSTGRES_PORT") or 5432
    database = os.getenv("POSTGRES_DATABASE_TEST") or "bookstest"

    SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    Base.metadata.create_all(engine)
    yield db
    db.close()
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db(clean_db):
    init_data(clean_db)
    return clean_db
