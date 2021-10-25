import os
import pdb
import sys

from database import engine
from elasticsearch import Elasticsearch
from models.author import AuthorORM
from models.book import BookORM
from scripts.read_epub import epubtohtml
from sqlalchemy.orm import Session

es = Elasticsearch(
    [os.getenv("ELASTIC_SEARCH_URL") or "localhost"],
    sniff_on_start=True,
    sniff_on_connection_fail=True,
    sniffer_timeout=60,
    port=os.getenv("ELASTIC_SEARCH_PORT") or 9201,
)


def get_book():
    res = es.search(index="books", query={"match_all": {}})
    for hit in res['hits']['hits']:
        print(hit["_id"])


def add_book(path):
    book_content = epubtohtml(path)
    if not book_content:
        return
    with Session(engine) as session:
        session.expire_on_commit = False
        authors = book_content.pop("author")
        book = BookORM(title=book_content.get("title", ""),
                       isbn=book_content.get("isbn", ""),
                       language=book_content.get("language", "en"))
        for au in authors:
            author = session.query(AuthorORM).filter(AuthorORM.first_name == au["first_name"],
                                                     AuthorORM.last_name == au["last_name"]).first()
            if not author:
                author = AuthorORM(first_name=au["first_name"], last_name=au["last_name"])
                session.add(author)
                session.flush()
            book.authors.append(author)
        session.add(book)
        session.commit()
        book_content["external_id"] = book.id
        res = es.index(index="books", body=book_content)
    print(book.id)
    print(res["result"])


def add_all_books_in_dir(dir, action):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".epub"):
                action(os.path.join(root, file))


def delete_books():
    with Session(engine) as session:
        session.expire_on_commit = False
        books = session.query(BookORM).all()
        for book in books:
            res = es.search(index="books", query={"constant_score": {"filter": {"term": {"external_id": book.id}}}})
            for hit in res['hits']['hits']:
                es_id = (hit["_id"])
            es.delete(index="books", id=es_id)
            session.delete(book)
        session.commit()


if __name__ == '__main__':
    path = sys.argv[1]
    delete_books()
    add_all_books_in_dir(path, add_book)
