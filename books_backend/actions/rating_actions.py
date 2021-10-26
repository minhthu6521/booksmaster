from sqlalchemy.orm import Session

from models.book import BookORM
from models.rating import RatingORM
from models.user import UserORM


def update_user_rating(db: Session, book: BookORM, user: UserORM, score: float, review: str = ""):
    rating = db.query(RatingORM).filter(RatingORM.book_id == book.id,
                                        RatingORM.user_id == user.id).first()
    if not rating:
        rating = RatingORM(book_id=book.id, user_id=user.id)
        db.add(rating)
    rating.score = score
    if review:
        rating.review = review
    db.flush()
    return book