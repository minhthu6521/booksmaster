from sqlalchemy import distinct
from sqlalchemy import func
from sqlalchemy import and_
from sqlalchemy import or_
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

_used = and_, or_


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
                self.columns.append(ColumnDefinition(column=col, type=data_type, possible_values=possible_values,
                                                     label=col.info.get("label")))

    def get_all_possible_columns_for_query(self):
        result = []
        for col in self.columns:
            result.append(col.to_pydantic_mode())
        return result

    def transform_to_db_column(self, col: Column):
        query_col = sql_col = next(x.column for x in self.columns if x.to_pydantic_mode().name == col.name)
        _cls = self.get_class_by_tablename(sql_col.table)
        class_col = getattr(_cls, sql_col.name)
        if col.operation:
            for op in col.operation:
                query_col = getattr(func, op)(query_col)
                class_col = getattr(func, op)(class_col)
        if col.label:
            query_col = query_col.label(col.label.lower().replace(" ", "_"))
        return query_col, sql_col, class_col

    def get_class_by_tablename(self, tablename):
        for c in self.models:
            if c.__tablename__ == str(tablename):
                return c

    def get_class_by_string(self, name):
        for c in self.models:
            if c.__name__ == name:
                return c

    def _gets_to_query(self, _query, configuration):
        gets = []
        columns = []
        for get_column in configuration:
            query_col, sql_col, _ = self.transform_to_db_column(get_column)
            gets.append(query_col)
            columns.append(sql_col)
        _query = _query.query(*gets)
        return self._join_to_query(_query, columns)

    def _join_to_query(self, _query, columns):
        if not all(x.table.name == columns[0].table.name for x in columns):
            join_classes = [self.get_class_by_tablename(c.table) for c in columns]
            join_classes_names = [jc.__name__ for jc in join_classes]
            inst = inspect(join_classes[0])
            for key, _relationship in inst.relationships.items():
                if _relationship.argument in join_classes_names:
                    _query = _query.join(getattr(join_classes[0], key), isouter=True)
        return _query

    def _groups_to_query(self, _query, configuration):
        if not configuration:
            return _query
        groups = []
        for group_column in configuration:
            groups.append(self.transform_to_db_column(group_column)[1])
        _query = _query.group_by(*groups)
        return _query

    def _filter_to_query(self, _query, configuration):
        if not configuration:
            return _query
        _filter = configuration.parse_to_sqlalchemy(self.transform_to_db_column)
        for model in self.models:
            _filter = _filter.replace(model.__name__, f"self.get_class_by_string('{model.__name__}')")
        _query = _query.filter(eval(_filter))
        return _query

    def _order_by_to_query(self, _query, configuration):
        if not configuration:
            return _query
        _orders = []
        for order_column in configuration:
            col = self.transform_to_db_column(order_column.item)[2]
            if order_column.direction == "desc":
                _orders.append(col.desc())
        _query = _query.order_by(*_orders)
        return _query

    def generate_get_query(self, configuration: QueryConfiguration, db: Session):
        _query = db
        _query = self._gets_to_query(_query, configuration.gets)
        _query = self._groups_to_query(_query, configuration.groups)
        _query = self._filter_to_query(_query, configuration.filters)
        _query = self._order_by_to_query(_query, configuration.orders)
        if configuration.limit:
            _query = _query.limit(configuration.limit)
        print(_query)
        return _query

    def get_query_result(self, query: Query):
        return [dict(row) for row in query.all()]

    def get_stat_data(self, configuration: QueryConfiguration, db: Session):
        _query = self.generate_get_query(configuration, db)
        result = self.get_query_result(_query)
        return result
