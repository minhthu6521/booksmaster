from typing import List
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session

from actions.book_actions import get_book_by_id
from actions.genre_actions import add_genre_to_book
from actions.genre_actions import do_update_book_genre
from actions.genre_actions import get_genre_by_id
from actions.genre_actions import get_or_create_genre
from actions.genre_actions import remove_genre
from actions.genre_actions import remove_genre_from_book
from actions.genre_actions import update_genre_name
from app import app
from database import get_db
from models.book import Book
from models.book import Genre
from models.book import GenreBase
from models.book import GenreORM
from models.book import GenreUpdate


@app.get("/api/genres/{genre_id}", response_model=Genre)
def get_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = get_genre_by_id(db, genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre


@app.get("/api/genres", response_model=List[Genre])
def get_genres(skip: int = 0, limit: int = 1000, q: Optional[str] = None, db: Session = Depends(get_db)):
    genre_query = db.query(GenreORM)
    if q:
        genre_query = genre_query.fillter(GenreORM.name.like(f"%{q}%"))
    genres = genre_query.offset(skip).limit(limit).all()
    return genres


@app.patch("/api/genres/{genre_id}", response_model=Genre)
def edit_genre_name(genre_id: int, data: GenreBase, db: Session = Depends(get_db)):
    genre = get_genre_by_id(db, genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    genre = update_genre_name(db, genre, data.name)
    db.commit()
    return genre


@app.delete("/api/genres/{genre_id}", status_code=204)
def delete_genre(genre_id: int, db: Session = Depends(get_db)):
    genre = get_genre_by_id(db, genre_id)
    if genre is None:
        raise HTTPException(status_code=404, detail="Genre not found")
    remove_genre(db, genre)
    db.commit()


@app.patch("/api/books/{book_id}/genres/{genre_name}", response_model=Book)
async def add_book_genre(book_id: int, genre_name: str, db: Session = Depends(get_db)):
    book = get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    genre = get_or_create_genre(db, genre_name)
    add_genre_to_book(db, genre, book)
    db.commit()
    return book


@app.delete("/api/books/{book_id}/genres/{genre_name}", response_model=Book)
async def delete_book_genre(book_id: int, genre_name: str, db: Session = Depends(get_db)):
    book = get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    genre = get_or_create_genre(db, genre_name)
    remove_genre_from_book(db, genre, book)
    db.commit()
    return book


@app.patch("/api/books/{book_id}/genres", response_model=Book)
async def update_book_genre(book_id: int, genres: List[GenreUpdate], db: Session = Depends(get_db)):
    book = get_book_by_id(book_id, db)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    do_update_book_genre(db, genres, book)
    db.commit()
    return book