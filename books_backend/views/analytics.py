from copy import deepcopy
from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from app import query_builder
from actions.default_configuration import DEFAULT_BOOK_STATISTICS_PAGE_CONFIGURATION
from actions.default_configuration import DEFAULT_MAIN_STATISTICS_PAGE_CONFIGURATION
from query_builder.models import ColumnQuery
from query_builder.models import QueryConfiguration
from query_builder.models import StatItem
from app import app
from database import get_db


@app.get("/api/query_builder/metadata/columns", response_model=List[ColumnQuery])
def get_data_columns_for_query_builder():
    return query_builder.get_all_possible_columns_for_query()


@app.get("/api/query_builder/query")
def query_stats(config: QueryConfiguration, db: Session = Depends(get_db)):
    result = query_builder.get_stat_data(config, db)
    return result


@app.get("/api/query_builder/configuration", response_model=List[StatItem])
def get_main_statistics_page_configuration(db: Session = Depends(get_db)):
    return deepcopy(DEFAULT_MAIN_STATISTICS_PAGE_CONFIGURATION)


@app.get("/api/query_builder/configuration/books", response_model=List[StatItem])
def get_book_statistics_page_configuration(db: Session = Depends(get_db)):
    return deepcopy(DEFAULT_BOOK_STATISTICS_PAGE_CONFIGURATION)
