from models.book import BookORM
from models.book import GenreORM
from sqlalchemy.orm import Session


def get_genre(db: Session, genre_name: str):
    genre = db.query(GenreORM).filter(GenreORM.name == genre_name).first()
    return genre


def add_genre(db: Session, genre_name: str):
    genre = GenreORM(name=genre_name)
    db.add(genre)
    db.flush()
    return genre


def get_or_create_genre(db: Session, genre_name: str):
    genre = get_genre(db, genre_name)
    if not genre:
        genre = add_genre(db, genre_name)
    return genre


def add_genre_to_book(db: Session, genre: GenreORM, book: BookORM):
    book.genres.append(genre)
    db.flush()
    return book
