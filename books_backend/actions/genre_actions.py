from typing import List

from sqlalchemy.orm import Session

from models.book import BookORM
from models.book import Genre
from models.book import GenreORM
from models.book import GenreUpdate


def get_genre_by_id(db: Session, genre_id: int):
    genre = db.query(GenreORM).filter(GenreORM.id == genre_id).first()
    return genre


def get_genre(db: Session, genre_name: str):
    genre = db.query(GenreORM).filter(GenreORM.name == genre_name).first()
    return genre


def update_genre_name(db: Session, genre: GenreORM, new_name: str):
    if db.query(GenreORM).filter(GenreORM.name == new_name).first():
        return None
    genre.name = new_name.strip()
    db.flush()
    return genre


def add_genre(db: Session, genre_name: str):
    genre = GenreORM(name=genre_name)
    db.add(genre)
    db.flush()
    return genre


def get_or_create_genre(db: Session, genre_name: str):
    genre_name = genre_name.capitalize()
    genre = get_genre(db, genre_name)
    if not genre:
        genre = add_genre(db, genre_name)
    return genre


def add_genre_to_book(db: Session, genre: GenreORM, book: BookORM):
    book.genres.append(genre)
    db.flush()
    return book


def remove_genre_from_book(db: Session, genre: GenreORM, book: BookORM):
    book.genres.remove(genre)
    db.flush()
    return book


def remove_genre(db: Session, genre: GenreORM):
    db.delete(genre)
    db.flush()


def do_update_book_genre(db: Session, genres: List[GenreUpdate], book: BookORM):
    current_genres = [g.name for g in book.genres]
    new_genres = [n.name for n in genres]

    _add_names = set(new_genres) - set(current_genres)
    _add = [get_or_create_genre(db, _a) for _a in _add_names]

    _remove_names = set(current_genres) - set(new_genres)
    _remove = [x for x in current_genres if x.name in _remove_names]
    for _a in _add:
        book.genres.append(_a)
    for _r in _remove:
        book.genres.remove(_r)
    db.flush()