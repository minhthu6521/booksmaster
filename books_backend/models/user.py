from typing import Optional

from sqlalchemy.orm import relationship

from database import Base
from database import get_db
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Session


class UserORM(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    first_name = Column(String)
    last_name = Column(String)
    ratings = relationship("RatingORM", back_populates="user")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool


def fake_decode_token(token, db: Session = Depends(get_db)):
    return db.query(UserORM).first()


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = fake_decode_token(token, db)
    return user
