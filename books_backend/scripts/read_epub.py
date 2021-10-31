from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT
from ebooklib import epub
from nltk.corpus import wordnet

NOT_READ_TAGS = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', 'style']


def strip_metadata(metadata):
    return metadata[0][0] if len(metadata) else ""


def html2text(html, not_read=NOT_READ_TAGS):
    if not html:
        return ""
    output = ''
    soup = BeautifulSoup(html)
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in not_read:
            output += '{} '.format(t)
    return output


def is_valid_eng_tags(tag):
    if not tag:
        return
    tag = tag.title().strip()
    tag_child = tag.split(" ")
    for t in tag_child:
        if not wordnet.synsets(t):
            return
    return tag


def split_author(author):
    if "," not in author:
        author_to_json = {
            "first_name": " ".join(author.split(" ")[:-1]),
            "last_name": author.split(" ")[-1]
        }
    else:
        author_to_json = {
            "first_name": author.split(",")[1],
            "last_name": author.split(",")[0]
        }
    return author_to_json


def epubtohtml(path):
    try:
        book = epub.read_epub(path)
    except:
        return
    read_metadata = lambda x, y: strip_metadata(book.get_metadata(x, y))
    title = read_metadata('DC', 'title')
    authors = read_metadata('DC', 'creator')
    if ";" in authors:
        authors = authors.split(";")
    else:
        authors = authors.split("&")
    _raw_tags = book.get_metadata('DC', 'subject')
    tags = None
    if _raw_tags:
        if not isinstance(_raw_tags, list):
            _raw_tags = _raw_tags.split("/")
        else:
            _raw_tags = [t[0] for t in _raw_tags]
        tags = [is_valid_eng_tags(t) for t in _raw_tags] if _raw_tags else None
        tags = [t for t in tags if t]
    authors_json = []
    for author in authors:
        authors_json.append(split_author(author))
    isbn = read_metadata('DC', 'identifier')
    language = read_metadata('DC', 'language') or "en"
    description = html2text(read_metadata('DC', 'description'))
    chapters = [item.get_content() for item in book.get_items() if item.get_type() == ITEM_DOCUMENT]
    content = [html2text(chapter) for chapter in chapters]
    content_text = "\n".join(content)
    content_html = b"".join(chapters).decode("utf-8")
    return {
        "title": title,
        "author": authors_json,
        "isbn": isbn,
        "language": language,
        "description": description,
        "content": content_text,
        "html": content_html,
        "tags": tags
    }


if __name__ == '__main__':
    print(epubtohtml())
