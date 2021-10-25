from typing import List
from typing import Optional

from actions.book_actions import get_book_by_id
from actions.genre_actions import add_genre_to_book
from actions.genre_actions import get_or_create_genre
from database import get_db
from fastapi import Depends
from fastapi import HTTPException
from models.book import Book
from models.book import BookORM
from models.user import UserORM
from models.user import get_current_user
from sqlalchemy.orm import Session
from views.utils import app


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/books", response_model=List[Book])
def get_books(skip: int = 0, limit: int = 100, q: Optional[str] = None, db: Session = Depends(get_db)):
    books_query = db.query(BookORM)
    if q:
        books_query = books_query.fillter(BookORM.title.like(f"%{q}%"))
    books = books_query.offset(skip).limit(limit).all()
    return books


@app.patch("/api/books/{book_id}/genres/{genre_name}", response_model=Book)
async def update_book_genre(book_id: int, genre_name: str, db: Session = Depends(get_db)):
    book = get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    genre = get_or_create_genre(db, genre_name)
    add_genre_to_book(db, genre, book)
    db.commit()
    return book
