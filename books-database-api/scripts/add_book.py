import sys
import os
from read_epub import epubtohtml
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from database import es

def get_book():
    res = es.search(index="books", query={"match_all": {}})
    for hit in res['hits']['hits']:
        print(hit["_id"])

def add_book(path):
    book_content = epubtohtml(path)
    res = es.index(index="books", body=book_content)
    print(res["result"])

if __name__ == '__main__':
    path = sys.argv[1]
    add_book(path)


