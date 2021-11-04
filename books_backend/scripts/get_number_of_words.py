import os

from sqlalchemy.orm import Session

from database import engine
from elasticsearch import Elasticsearch

from models.book import BookORM

es = Elasticsearch(
    [os.getenv("ELASTIC_SEARCH_URL") or "localhost"],
    sniff_on_start=True,
    sniff_on_connection_fail=True,
    sniffer_timeout=60,
    port=os.getenv("ELASTIC_SEARCH_PORT") or 9201,
)


def update_number_of_words_per_book():
    with Session(engine) as session:
        session.expire_on_commit = False
        books = session.query(BookORM).all()
        for book in books:
            res = es.search(index="books", query={"constant_score": {"filter": {"term": {"external_id": book.id}}}})
            for hit in res['hits']['hits']:
                r = es.get(index="books", id=hit["_id"])
                content = r['_source']["content"]
                content_length = len(content.split())
            book.content_length = content_length
        session.commit()


if __name__ == '__main__':
    update_number_of_words_per_book()