import os
import pdb
import sys

from database import engine
from elasticsearch import Elasticsearch
from models.author import AuthorORM
import xml.etree.ElementTree as ET
from models.book import BookORM
from models.book import GenreORM
from scripts.read_epub import epubtohtml
from sqlalchemy.orm import Session

from scripts.read_epub import split_author

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


def get_metadata_from_file(metadata_file):
    tree = ET.parse(metadata_file)
    result = {
    }
    elements = tree.find('{http://www.idpf.org/2007/opf}metadata')
    for el in elements:
        if "title" in el.tag:
            result["title"] = el.text
        elif "creator" in el.tag:
            result.setdefault("author", [])
            result["author"].append(split_author(el.text))
        elif "language" in el.tag:
            result["language"] = el.text
        elif "subject" in el.tag:
            result.setdefault("tags", [])
            result["tags"].append(el.text)
        elif "description" in el.tag:
            result["description"] = el.text
        elif "identifier" in el.tag and el.attrib.get("{http://www.idpf.org/2007/opf}scheme") == "ISBN":
            result["isbn"] = el.text
    return result


def add_book(path, metadata_file=None):
    book_content = epubtohtml(path)
    if not book_content:
        return
    if metadata_file:
        metadata = get_metadata_from_file(metadata_file)
        book_content.update(metadata)
    with Session(engine) as session:
        session.expire_on_commit = False
        authors = book_content.pop("author")
        tags = book_content["tags"]
        book = BookORM(title=book_content.get("title", ""),
                       isbn=book_content.get("isbn", ""),
                       language=book_content.get("language", "en"),
                       description=book_content.get("description", ""))
        for au in authors:
            author = session.query(AuthorORM).filter(AuthorORM.first_name == au["first_name"],
                                                     AuthorORM.last_name == au["last_name"]).first()
            if not author:
                author = AuthorORM(first_name=au["first_name"], last_name=au["last_name"])
                session.add(author)
                session.flush()
            book.authors.append(author)
        if tags:
            for tag in tags:
                genre = session.query(GenreORM).filter(GenreORM.name == tag).first()
                if not genre:
                    genre = GenreORM(name=tag)
                    session.add(genre)
                    session.flush()
                book.genres.append(genre)
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
                action(os.path.join(root, file), metadata_file=os.path.join(root, "metadata.opf"))


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


def delete_book(book_id):
    with Session(engine) as session:
        session.expire_on_commit = False
        book = session.query(BookORM).get(book_id)
        res = es.search(index="books", query={"constant_score": {"filter": {"term": {"external_id": book.id}}}})
        for hit in res['hits']['hits']:
            es_id = (hit["_id"])
        es.delete(index="books", id=es_id)
        session.delete(book)
        session.commit()


if __name__ == '__main__':
    path = sys.argv[1]
    metadata = path.split("/")[:-1]
    metadata = "/".join(metadata) + "/metadata.opf"
    #delete_books()
    #add_all_books_in_dir(path, add_book)
    add_book(path, metadata)