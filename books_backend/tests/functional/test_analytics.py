from query_builder.main import DataQueryBuilder
from query_builder.models import Column
from query_builder.models import QueryConfiguration


def test_generate_query(db, test_book_data):
    col1 = Column(name="rating.score", label="rating")
    col2 = Column(name="users.first_name", label="user")
    col3 = Column(name="books.title", label="book")
    configuration = QueryConfiguration(gets=[col1, col2, col3])
    query_builder = DataQueryBuilder(db=db)
    _query = query_builder.generate_get_query(configuration, db)
    result = query_builder.get_query_result(_query)
    assert result == [{'rating': 3.0, 'user': 'test', 'book': 'Book 1'},
                      {'rating': 5.0, 'user': 'test', 'book': 'Book 1'}]

    col1 = Column(name="rating.score", label="rating", operation=["avg"])
    configuration = QueryConfiguration(gets=[col1])
    _query = query_builder.generate_get_query(configuration, db)
    result = query_builder.get_query_result(_query)
    assert result == [{'rating': 4.0}]