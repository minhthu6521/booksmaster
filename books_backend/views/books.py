from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.book import Book
from models.book import BookORM

from views.utils import app


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookORM).filter(BookORM.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/books", response_model=List[Book])
def get_users(skip: int = 0, limit: int = 100, q: Optional[str] = None, db: Session = Depends(get_db)):
    books_query = db.query(BookORM)
    if q:
        books_query = books_query.fillter(BookORM.title.like(f"%{q}%"))
    books = books_query.offset(skip).limit(limit).all()
    return books

