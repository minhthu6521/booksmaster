from analytics.main import generate_get_query
from analytics.main import get_query_result
from analytics.models import Column
from analytics.models import QueryConfiguration


def test_generate_query(db, test_book_data):
    col1 = Column(name="rating.score", label="rating")
    col2 = Column(name="users.first_name", label="user")
    col3 = Column(name="books.title", label="book")
    configuration = QueryConfiguration(gets=[col1, col2, col3])
    _query = generate_get_query(configuration, db)
    result = get_query_result(_query)
    assert result == [{'rating': 3.0, 'user': 'test', 'book': 'Book 1'},
                      {'rating': 5.0, 'user': 'test', 'book': 'Book 1'}]

    col1 = Column(name="rating.score", label="rating", operation=["avg"])
    configuration = QueryConfiguration(gets=[col1])
    _query = generate_get_query(configuration, db)
    result = get_query_result(_query)
    assert result == [{'rating': 4.0}]