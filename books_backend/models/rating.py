from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.orm import relationship

from analytics import for_analytics
from database import Base


@for_analytics
class RatingORM(Base):
    __tablename__ = "rating"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id', name='rating_book_id'))
    user_id = Column(Integer, ForeignKey('users.id', name='rating_user_id'))
    book = relationship("BookORM", back_populates="ratings")
    user = relationship("UserORM", back_populates="ratings")
    review = Column(Text)
    score = Column(Float)


class RatingBase(BaseModel):
    id: int
    score: float
    user_id: int
    review: Optional[str]

    class Config:
        orm_mode = True
