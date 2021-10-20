import sys
import os
from read_epub import epubtohtml
from books_database_api.database import es


def get_book():
    res = es.search(index="books", query={"match_all": {}})
    for hit in res['hits']['hits']:
        print(hit["_id"])


def add_book(path, id):
    book_content = epubtohtml(path)
    res = es.index(index="books", body=book_content, id=id)
    print(res["result"])


def add_all_books_in_dir(dir, action):
    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".epub"):
                action(os.path.join(root, file))


def delete_book(id):
    es.delete(index="books", id=id)


if __name__ == '__main__':
    path = sys.argv[1]
    get_book()
