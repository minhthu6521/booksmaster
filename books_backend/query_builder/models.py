from typing import List
from typing import Optional
from typing import Union

from models.utils import PropertyBaseModel
from query_builder import CLAUSES
from query_builder import OPERATIONS
from query_builder import VALUES


class PossibleValue(PropertyBaseModel):
    label: str
    value: Union[str, int]


class ColumnQuery(PropertyBaseModel):
    name: str
    data_type: str
    possible_values: Optional[List[PossibleValue]]
    label: Optional[str]


class ColumnDefinition(object):
    column = None
    type = None
    label = None
    possible_values = None

    def __init__(self, column, type, possible_values=None, label=None):
        self.column = column
        self.type = type
        self.possible_values = possible_values
        self.label = label

    def to_pydantic_mode(self):
        return ColumnQuery(name=f"{self.column.table.name}.{self.column.name}",
                           data_type=self.type,
                           possible_values=self.possible_values,
                           label=self.label)


class Column(PropertyBaseModel):
    name: str
    operation: Optional[List[str]]
    label: Optional[str]


class FilterSubItem(PropertyBaseModel):
    item: Column
    clause: str
    value: Optional[str]

    def parse_to_sqlalchemy(self, get_col_func):
        column = get_col_func(self.item)[2]
        value = self.value
        if value is not None and value in VALUES.keys():
            value = VALUES[value]
        return CLAUSES[self.clause](column, value)


class FilterLiteralItem(PropertyBaseModel):
    literal: str

    def parse_to_sqlalchemy(self, get_col_func):
        return self.literal


class FilterItem(PropertyBaseModel):
    items: List[dict]
    operation: str

    def parse_to_sqlalchemy(self, get_col_func):
        operation = self.operation
        _filters = []
        for item in self.items:
            if item.get("operation"):
                item_cls = FilterItem
            elif item.get("literal"):
                item_cls = FilterLiteralItem
            else:
                item_cls = FilterSubItem
            item_cls = item_cls.parse_obj(item)
            _query_filter = item_cls.parse_to_sqlalchemy(get_col_func)
            _filters.append(_query_filter)
        return OPERATIONS[operation](_filters)


class OrderItem(PropertyBaseModel):
    item: Column
    direction: str = "asc"


class QueryConfiguration(PropertyBaseModel):
    gets: List[Column]
    filters: Optional[FilterItem]
    groups: Optional[List[Column]]
    limit: Optional[int]
    orders: Optional[List[OrderItem]]


class DisplayConfiguration(PropertyBaseModel):
    title: str
    type: str
    description: Optional[str]
    xAxis: Optional[str]
    yAxis: Optional[str]
    yAxisLabel: Optional[str]
    item: Optional[str]
    name: Optional[str]
    value: Optional[str]
    width: Optional[str]
    height: Optional[str]


class StatItem(PropertyBaseModel):
    id: str
    query_configuration: QueryConfiguration
    display_configuration: Optional[DisplayConfiguration]
