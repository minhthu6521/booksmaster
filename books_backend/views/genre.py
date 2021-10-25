from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.book import Book
from models.book import BookORM

from views.utils import app

from models.book import GenreORM

from models.book import Genre


@app.get("/genre/{genre_id}", response_model=Genre)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = db.query(GenreORM).filter(BookORM.id == genre_id).first()
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@app.get("/genre", response_model=List[Genre])
def get_users(skip: int = 0, limit: int = 100, q: Optional[str] = None, db: Session = Depends(get_db)):
    genre_query = db.query(GenreORM)
    if q:
        genre_query = genre_query.fillter(GenreORM.title.like(f"%{q}%"))
    genres = genre_query.offset(skip).limit(limit).all()
    return genres

