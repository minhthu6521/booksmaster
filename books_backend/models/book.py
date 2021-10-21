from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from typing import List, Optional

from pydantic import BaseModel

from database import Base


class BookORM(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    isbn = Column(String)
    language = Column(String(5))


class Book(BaseModel):
    id: int
    title: str
    isbn: Optional[str] = None

    class Config:
        orm_mode = True
