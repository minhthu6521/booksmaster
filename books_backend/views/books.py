from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from actions.book_actions import get_book_by_id
from actions.book_actions import remove_book
from actions.book_actions import update_book_metadata
from actions.rating_actions import update_user_rating
from app import app
from database import get_db
from models.book import Book
from models.book import BookBase
from models.book import BookORM
from models.user import get_current_user


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
        books_query = books_query.filter(BookORM.title.ilike(f"%{q}%"))
    books = books_query.offset(skip).limit(limit).all()
    return books


@app.put("/api/books/{book_id}", response_model=Book)
async def update_book_metadata_api(book_id: int, book_json: BookBase, db: Session = Depends(get_db)):
    book = get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book = update_book_metadata(book, book_json)
    db.commit()
    return book


@app.patch("/api/books/{book_id}/ratings/{score}", response_model=Book)
async def patch_user_rating(book_id: int, score: float, db: Session = Depends(get_db)):
    book = get_book_by_id(book_id, db)
    user = get_current_user(db)  # TODO: Change everywhere
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    book = update_user_rating(db, book, user, score)
    db.commit()
    return book


@app.delete("/api/books/{book_id}", response_model=Book)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    remove_book(book, db)
    db.commit()
    return
