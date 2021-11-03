from analytics.main import generate_get_query
from analytics.models import Column
from analytics.models import QueryConfiguration


def test_generate_query(db, test_book_data):
    col1 = Column(name="rating.score", label="rating")
    configuration = QueryConfiguration(gets=[col1])
    result = generate_get_query(configuration, db)
    print(result)