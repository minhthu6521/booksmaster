from database import es

from models.word_cloud import WordCloud
from models.word_cloud import WordFrequency
from CleanText import clean_data


def get_book_content(ext_id: int, language=None):
    filters = {"external_id": ext_id}
    if language:
        filters["language"] = language
    res = es.search(index="books", query={"constant_score": {"filter": {"term": filters}}})
    if len(res['hits']['hits']) != 1:
        return
    return res['hits']['hits'][0]["_source"]['content']


def get_word_cloud_of_book_content(ext_id: int, min_occurence: int = 10):
    content = get_book_content(ext_id)
    if not content:
        return
    list_of_words = clean_data.clean_text(content)
    wordcloud = WordCloud(words=[])
    distinct = set(list_of_words)
    for key in distinct:
        occurence = list_of_words.count(key)
        if occurence >= min_occurence:
            word = WordFrequency(text=key, value=list_of_words.count(key))
            wordcloud.words.append(word)
    return wordcloud
