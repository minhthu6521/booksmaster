from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from analytics.actions import get_all_possible_columns_for_query
from analytics.main import get_stat_data
from analytics.models import ColumnQuery
from analytics.models import StatItem
from database import get_db
from app import app


@app.get("/api/analytics/metadata/columns", response_model=List[ColumnQuery])
def get_data_columns_for_query_builder():
    return get_all_possible_columns_for_query()


@app.get("/api/analytics/query")
def query_stats(config: StatItem, db: Session = Depends(get_db)):
    result = get_stat_data(config, db)
    return result