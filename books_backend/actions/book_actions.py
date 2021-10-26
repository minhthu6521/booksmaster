from fastapi import Depends
from sqlalchemy.orm import Session

from database import get_db
from models.book import BookBase
from models.book import BookORM


def get_book_by_id(book_id: int, db: Session):
    book = db.query(BookORM).filter(BookORM.id == book_id).first()
    return book


def update_book_metadata(book: BookORM, json_data: BookBase):
    book.title = json_data.title or book.title
    book.isbn = json_data.isbn or book.isbn
    return book
