from typing import List
from typing import Optional

from database import Base
from models.author import AuthorBase
from models.author import book_author_table
from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship


class RatingORM(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id', name='rating_book_id'))
    user_id = Column(Integer, ForeignKey('users.id', name='rating_user_id'))
    book = relationship("BookORM", back_populates="ratings")
    user = relationship("UserORM", back_populates="ratings")


class Rating(BaseModel):
    id: int
    title: str
    isbn: Optional[str] = None

    class Config:
        orm_mode = True
