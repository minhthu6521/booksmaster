from sqlalchemy import func
from sqlalchemy.orm import Session

from analytics import COLUMN_LISTS
from analytics.models import Column
from analytics.models import QueryConfiguration
from analytics.models import StatItem


def transform_to_db_column(col: Column):
    print([x.column.name for x in COLUMN_LISTS])
    sql_col = next(x for x in COLUMN_LISTS if x.column.name == col.name)
    if col.label:
        sql_col = sql_col.label(col.label)
    if not col.operation:
        return sql_col
    for op in col.operation:
        sql_col = getattr(func, op)(sql_col)
    return sql_col


def generate_get_query(configuration: QueryConfiguration, db: Session):
    _query = db
    gets = []
    for get_column in configuration.gets:
        gets.append(transform_to_db_column(get_column))
    _query = _query.query(*gets)
    return _query


def get_stat_data(configuration: StatItem, db: Session):
    pass
