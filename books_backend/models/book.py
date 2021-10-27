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

from models.rating import RatingBase
from models.user import User

book_genre_table = Table('book_genre', Base.metadata,
                         Column('book_id', ForeignKey('books.id', name="book_genre_fk"), primary_key=True),
                         Column('genre_id', ForeignKey('genre.id', name="genre_book_fk"), primary_key=True),
                         )


class BookORM(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    isbn = Column(String)
    language = Column(String(5))
    description = Column(Text)
    genres = relationship(
        "GenreORM",
        secondary=book_genre_table,
        back_populates="books"
    )
    authors = relationship("AuthorORM",
                           secondary=book_author_table,
                           back_populates="books")
    ratings = relationship("RatingORM", back_populates="book")


class BookBase(BaseModel):
    id: int
    title: str
    isbn: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


class GenreORM(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    books = relationship(
        "BookORM",
        secondary=book_genre_table,
        back_populates="genres"
    )


class GenreBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Genre(GenreBase):
    books: List[BookBase] = []


class Book(BookBase):
    genres: List[GenreBase] = []
    authors: List[AuthorBase] = []
    ratings: List[RatingBase] = []


class Author(AuthorBase):
    books: List[Book] = []


class Rating(RatingBase):
    book: Book
    user: User
