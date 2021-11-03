from sqlalchemy import func
from sqlalchemy import inspect
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session

from analytics import COLUMN_LISTS
from analytics import MODELS
from analytics.models import Column
from analytics.models import QueryConfiguration
from analytics.models import StatItem
from database import Base


def transform_to_db_column(col: Column):
    sql_col = next(x.column for x in COLUMN_LISTS if x.to_pydantic_mode().name == col.name)
    if col.operation:
        for op in col.operation:
            sql_col = getattr(func, op)(sql_col)
    if col.label:
        sql_col = sql_col.label(col.label)
    return sql_col


def get_class_by_tablename(tablename):
    for c in MODELS:
        if c.__tablename__ == str(tablename):
            return c


def get_class_by_string(name):
    for c in MODELS:
        if c.__name__ == name:
            return c


def generate_get_query(configuration: QueryConfiguration, db: Session):
    _query = db
    gets = []
    for get_column in configuration.gets:
        gets.append(transform_to_db_column(get_column))
    _query = _query.query(*gets)

    _join_column = next(x.column for x in COLUMN_LISTS if x.to_pydantic_mode().name == configuration.gets[0].name)
    inst = inspect(get_class_by_tablename(_join_column.table))
    for _relationship in inst.relationships.values():
        _query = _query.join(get_class_by_string(_relationship.argument), _relationship.primaryjoin, isouter=True)

    if configuration.group:
        groups = []
        for group_column in configuration.group:
            groups.append(transform_to_db_column(group_column))
        _query = _query.group_by(*groups)
    print(_query)
    return _query


def get_query_result(query: Query):
    return [dict(row) for row in query.all()]


def get_stat_data(configuration: StatItem, db: Session):
    pass
