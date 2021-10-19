from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT
from ebooklib import epub

NOT_READ_TAGS = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script', 'style']


def strip_metadata(metadata):
    return metadata[0][0]


def html2text(html, not_read=NOT_READ_TAGS):
    output = ''
    soup = BeautifulSoup(html)
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in not_read:
            output += '{} '.format(t)
    return output


def epubtohtml(path):
    book = epub.read_epub(path)
    read_metadata = lambda x, y: strip_metadata(book.get_metadata(x, y))
    title = read_metadata('DC', 'title')
    author = read_metadata('DC', 'creator')
    isbn = read_metadata('DC', 'identifier')
    description = html2text(read_metadata('DC', 'description'))
    chapters = [item.get_content() for item in book.get_items() if item.get_type() == ITEM_DOCUMENT]
    content = [html2text(chapter) for chapter in chapters]
    return {
        "title": title,
        "author": author,
        "isbn": isbn,
        "description": description,
        "content": content
    }


if __name__ == '__main__':
    print(epubtohtml())
