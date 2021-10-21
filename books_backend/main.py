from fastapi import Depends
from fastapi import FastAPI
from fastapi import HTTPException
from typing import Optional

from database import SessionLocal
from models.book import Book
from models.book import BookORM
from sqlalchemy.orm import Session

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, q: Optional[str] = None, db: Session = Depends(get_db)):
    book = db.query(BookORM).filter(BookORM.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book