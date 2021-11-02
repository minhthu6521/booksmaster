from typing import List
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from analytics import for_analytics
from database import Base
from database import SessionLocal
from models.author import AuthorBase
from models.author import book_author_table
from models.rating import RatingBase
from models.user import User
from models.user import get_current_user
from models.utils import PropertyBaseModel
from analytics.utils import CATEGORIZED_DATA_TYPE

book_genre_table = Table('book_genre', Base.metadata,
                         Column('book_id', ForeignKey('books.id', name="book_genre_fk"), primary_key=True),
                         Column('genre_id', ForeignKey('genre.id', name="genre_book_fk"), primary_key=True),
                         )


@for_analytics
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


class BookBase(PropertyBaseModel):
    id: int
    title: str
    isbn: Optional[str] = None
    description: Optional[str] = None

    class Config:
        orm_mode = True


@for_analytics
class GenreORM(Base):
    __tablename__ = "genre"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, info={"data_type": CATEGORIZED_DATA_TYPE})
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

    @property
    def current_user_rating(self):
        db = SessionLocal()
        user = get_current_user(db)
        db.close()
        rating = next((x for x in self.ratings if x.user_id == user.id), None)
        return rating.score if rating else None


class Author(AuthorBase):
    books: List[Book] = []


class Rating(RatingBase):
    book: Book
    user: User
