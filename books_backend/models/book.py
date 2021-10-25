from typing import List
from typing import Optional

from database import Base
from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from models.author import AuthorBase

from models.author import book_author_table

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
    genres = relationship(
        "GenreORM",
        secondary=book_genre_table,
        back_populates="books"
    )
    authors = relationship("AuthorORM",
                           secondary=book_author_table,
                           back_populates="books")


class BookBase(BaseModel):
    id: int
    title: str
    isbn: Optional[str] = None

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


class Genre(BaseModel):
    id: int
    name: str
    books: List[BookBase] = []

    class Config:
        orm_mode = True


class Book(BookBase):
    genres: List[Genre] = []
    authors: List[AuthorBase] = []


class Author(AuthorBase):
    books: List[Book] = []
