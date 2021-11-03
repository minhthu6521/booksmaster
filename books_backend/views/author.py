from typing import List
from typing import Optional

from database import get_db
from fastapi import Depends
from fastapi import HTTPException
from models.author import AuthorORM
from models.book import Author
from sqlalchemy.orm import Session
from app import app


@app.get("/api/author/{author_id}", response_model=Author)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = db.query(AuthorORM).filter(AuthorORM.id == author_id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@app.get("/api/authors", response_model=List[Author])
def get_authors(skip: int = 0, limit: int = 100, q: Optional[str] = None, db: Session = Depends(get_db)):
    author_query = db.query(AuthorORM)
    if q:
        author_query = author_query.fillter(AuthorORM.title.like(f"%{q}%"))
    authors = author_query.offset(skip).limit(limit).all()
    return authors

