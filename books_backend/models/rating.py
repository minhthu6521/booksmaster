from typing import List
from typing import Optional

from sqlalchemy import Text

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

from models.book import Book
from models.user import User


class RatingORM(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id', name='rating_book_id'))
    user_id = Column(Integer, ForeignKey('users.id', name='rating_user_id'))
    book = relationship("BookORM", back_populates="ratings")
    user = relationship("UserORM", back_populates="ratings")
    review = Column(Text)


class RatingBase(BaseModel):
    id: int
    review: str

    class Config:
        orm_mode = True


class Rating(RatingBase):
    book: Book
    user: User
