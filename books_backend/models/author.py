from analytics import for_analytics
from database import Base
from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import relationship

book_author_table = Table('book_author', Base.metadata,
                          Column('book_id', ForeignKey('books.id', name="book_genre_fk"), primary_key=True),
                          Column('author_id', ForeignKey('author.id', name="author_book_fk"), primary_key=True),
                          )


@for_analytics
class AuthorORM(Base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    books = relationship("BookORM",
                         secondary=book_author_table,
                         back_populates="authors")


class AuthorBase(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True
