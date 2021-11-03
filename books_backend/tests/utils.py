import pytest

from app import list_columns
from models.book import BookORM
from models.book import GenreORM
from models.rating import RatingORM
from models.user import UserORM


def init_data(db):
    user = UserORM(first_name="test", last_name="user", email="test_user@example.com")
    db.add(user)
    list_columns(db)
    db.commit()


@pytest.fixture(scope="function")
def test_book_data(db):
    book1 = BookORM(title="Book 1", description="This is the first book", language="eng")
    book2 = BookORM(title="Learning Programming", description="How to program", language="eng")

    db.add_all([book1, book2])

    genre1 = GenreORM(name="Fiction")
    genre2 = GenreORM(name="Nonfiction")
    genre3 = GenreORM(name="Romance")

    db.add_all([genre1, genre2, genre3])

    db.flush()
    book1.genres.append(genre1)
    book1.genres.append(genre3)
    book2.genres.append(genre2)

    user = db.query(UserORM).first()
    rating1 = RatingORM(book_id=book1.id, user_id=user.id, score=3)
    rating2 = RatingORM(book_id=book1.id, user_id=user.id, score=5)
    db.add_all([rating1, rating2])

    db.flush()
