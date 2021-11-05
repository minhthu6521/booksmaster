from copy import deepcopy
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app import query_builder
from actions.default_stats_configuration import DEFAULT_BOOK_STATISTICS_PAGE_CONFIGURATION
from actions.default_stats_configuration import DEFAULT_MAIN_STATISTICS_PAGE_CONFIGURATION
from query_builder.models import ColumnQuery
from query_builder.models import QueryConfiguration
from query_builder.models import StatItem
from app import app
from database import get_db


@app.get("/api/statistics/metadata/columns", response_model=List[ColumnQuery])
def get_data_columns_for_statistics():
    return query_builder.get_all_possible_columns_for_query()


@app.post("/api/statistics/query")
def query_stats(config: QueryConfiguration, db: Session = Depends(get_db)):
    result = query_builder.get_stat_data(config, db)
    return result


@app.get("/api/statistics/configuration", response_model=List[StatItem])
def get_main_statistics_page_configuration(db: Session = Depends(get_db)):
    order = ["count_book_num", "completion_percentage",
             "average_num_words_per_text",
             "average_rating_text",
             "number_of_author_text",
             "number_of_books_per_genre",
             "most_read_genre",
             "average_rating_per_genre",
             "average_num_words_per_genre"]  # TODO :remove- this is for easier testing
    config = deepcopy(DEFAULT_MAIN_STATISTICS_PAGE_CONFIGURATION)
    config = sorted(config, key=lambda x: order.index(x["id"]))
    result = []
    for item in config:
        result.append(StatItem.parse_obj(item))
    return result


@app.get("/api/statistics/configuration/books", response_model=List[StatItem])
def get_book_statistics_page_configuration(db: Session = Depends(get_db)):
    return deepcopy(DEFAULT_BOOK_STATISTICS_PAGE_CONFIGURATION)
