from sqlalchemy import distinct
from sqlalchemy import func
from sqlalchemy import inspect
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session

from query_builder import CATEGORIZED_DATA_TYPE
from query_builder import MODELS
from query_builder import SQLALCHEMY_TYPES_TO_DATA_TYPE
from query_builder.models import Column
from query_builder.models import ColumnDefinition
from query_builder.models import PossibleValue
from query_builder.models import QueryConfiguration


class DataQueryBuilder(object):
    models = []
    columns = []

    def __init__(self, db):
        self.models = MODELS
        self.columns = []
        for cls in self.models:
            inst = inspect(cls)
            for col in inst.mapper.columns:
                data_type = col.info.get("data_type")
                possible_values = col.info.get("possible_values")
                if not data_type:
                    data_type = SQLALCHEMY_TYPES_TO_DATA_TYPE.get(col.type.__visit_name__)
                if data_type == CATEGORIZED_DATA_TYPE and not possible_values:
                    possible_values = [PossibleValue(label=v[0], value=v[0]) for v in db.query(distinct(col)).all()]
                self.columns.append(ColumnDefinition(column=col, type=data_type, possible_values=possible_values))

    def get_all_possible_columns_for_query(self):
        result = []
        for col in self.columns:
            result.append(col.to_pydantic_mode())
        return result

    def transform_to_db_column(self, col: Column):
        sql_col = next(x.column for x in self.columns if x.to_pydantic_mode().name == col.name)
        if col.operation:
            for op in col.operation:
                sql_col = getattr(func, op)(sql_col)
        if col.label:
            sql_col = sql_col.label(col.label)
        return sql_col

    def get_class_by_tablename(self, tablename):
        for c in self.models:
            if c.__tablename__ == str(tablename):
                return c

    def get_class_by_string(self, name):
        for c in self.models:
            if c.__name__ == name:
                return c

    def generate_get_query(self, configuration: QueryConfiguration, db: Session):
        _query = db
        gets = []
        for get_column in configuration.gets:
            gets.append(self.transform_to_db_column(get_column))
        _query = _query.query(*gets)

        _join_column = next(x.column for x in self.columns if x.to_pydantic_mode().name == configuration.gets[0].name)
        inst = inspect(self.get_class_by_tablename(_join_column.table))
        for _relationship in inst.relationships.values():
            _query = _query.join(self.get_class_by_string(_relationship.argument), _relationship.primaryjoin,
                                 isouter=True)

        if configuration.group:
            groups = []
            for group_column in configuration.group:
                groups.append(self.transform_to_db_column(group_column))
            _query = _query.group_by(*groups)
        print(_query)
        return _query

    def get_query_result(self, query: Query):
        return [dict(row) for row in query.all()]

    def get_stat_data(self, configuration: QueryConfiguration, db: Session):
        _query = self.generate_get_query(configuration, db)
        result = self.get_query_result(_query)
        return result


