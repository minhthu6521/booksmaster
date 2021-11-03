from typing import List
from typing import Optional

from models.utils import PropertyBaseModel


class ColumnDefinition(object):
    column = None
    type = None
    possible_values = None

    def __init__(self, column, type, possible_values=None):
        self.column = column
        self.type = type
        self.possible_values = possible_values
        print(possible_values)


class Column(PropertyBaseModel):
    name: str
    operation: Optional[str]
    label: Optional[str]


class FilterItem(PropertyBaseModel):
    item: Column
    clause: str
    value: Optional[str]


class QueryConfiguration(PropertyBaseModel):
    gets: List[Column]
    filters: List[FilterItem]
    group: List[Column]


class DisplayConfiguration(PropertyBaseModel):
    pass


class StatItem(PropertyBaseModel):
    query_configuration: QueryConfiguration
    display_configuration: DisplayConfiguration
