from typing import List
from typing import Optional
from typing import Union

from models.utils import PropertyBaseModel


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
        print(self.label)
        return ColumnQuery(name=f"{self.column.table.name}.{self.column.name}",
                           data_type=self.type,
                           possible_values=self.possible_values,
                           label=self.label)


class Column(PropertyBaseModel):
    name: str
    operation: Optional[List[str]]
    label: Optional[str]


class FilterItem(PropertyBaseModel):
    item: Column
    clause: str
    value: Optional[str]


class QueryConfiguration(PropertyBaseModel):
    gets: List[Column]
    filters: Optional[List[FilterItem]]
    groups: Optional[List[Column]]


class DisplayConfiguration(PropertyBaseModel):
    pass


class StatItem(PropertyBaseModel):
    query_configuration: QueryConfiguration
    display_configuration: Optional[DisplayConfiguration]
