from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from actions.book_actions import get_book_by_id
from actions.book_actions import update_book_metadata
from database import get_db
from models.book import Book
from models.book import BookBase
from models.book import BookORM
from views.utils import app


@app.get("/api/books/{book_id}", response_model=Book)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.get("/api/books", response_model=List[Book])
def get_books(skip: int = 0, limit: int = 100, q: Optional[str] = None, db: Session = Depends(get_db)):
    books_query = db.query(BookORM)
    if q:
        books_query = books_query.fillter(BookORM.title.like(f"%{q}%"))
    books = books_query.offset(skip).limit(limit).all()
    return books


@app.put("/api/books/{book_id}", response_model=Book)
async def update_book_metadata_api(book_id: int, book_json: BookBase, db: Session = Depends(get_db)):
    book = get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book = update_book_metadata(book, book_json, db)
    db.commit()
    return book