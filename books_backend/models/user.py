from typing import Optional

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship

from analytics import for_analytics
from database import Base


@for_analytics
class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    first_name = Column(String)
    last_name = Column(String)
    ratings = relationship("RatingORM", back_populates="user")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    id: int
    username: str
    email: str = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True


def get_current_user(db: Session):
    user = db.query(UserORM).first()
    return user
