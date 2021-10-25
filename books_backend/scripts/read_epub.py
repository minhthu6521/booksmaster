from bs4 import BeautifulSoup
from ebooklib import ITEM_DOCUMENT
from ebooklib import epub

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


def epubtohtml(path):
    try:
        book = epub.read_epub(path)
    except:
        return
    read_metadata = lambda x, y: strip_metadata(book.get_metadata(x, y))
    title = read_metadata('DC', 'title')
    authors = read_metadata('DC', 'creator')
    authors = authors.split(";")
    authors_json = []
    for author in authors:
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
        authors_json.append(author_to_json)
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
        "html": content_html
    }


if __name__ == '__main__':
    print(epubtohtml())
