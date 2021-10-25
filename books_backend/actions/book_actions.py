from models.book import BookORM


def get_book_by_id(book_id, db):
    book = db.query(BookORM).filter(BookORM.id == book_id).first()
    return book