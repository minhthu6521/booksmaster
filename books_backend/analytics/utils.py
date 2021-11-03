from sqlalchemy import distinct

from analytics.model import ColumnDefinition
from database import SessionLocal

BOOLEAN_DATA_TYPE = "boolean"
DATETIME_DATA_TYPE = "datetime"
DATE_DATA_TYPE = "date"
NUMBER_DATA_TYPE = "number"
CATEGORIZED_DATA_TYPE = "categorized"
RAW_TEXT_DATA_TYPE = "text"

COLUMN_TYPES = [BOOLEAN_DATA_TYPE, DATE_DATA_TYPE, DATETIME_DATA_TYPE, NUMBER_DATA_TYPE, CATEGORIZED_DATA_TYPE,
                RAW_TEXT_DATA_TYPE]

MODELS = []
COLUMN_LISTS = []

SQLALCHEMY_TYPES_TO_DATA_TYPE = {
    "date": DATE_DATA_TYPE,
    "datetime": DATETIME_DATA_TYPE,
    "string": RAW_TEXT_DATA_TYPE,
    "boolean": BOOLEAN_DATA_TYPE,
    "text": RAW_TEXT_DATA_TYPE,
    "float": NUMBER_DATA_TYPE,
    "integer": NUMBER_DATA_TYPE,
}


def for_analytics(cls):
    global COLUMN_LISTS
    MODELS.append(cls)
    COLUMN_LISTS += list_of_columns_in_class(cls)
    return cls


def list_of_columns_in_class(cls):
    columns = []
    db = SessionLocal()
    for col in cls.__table__.columns:
        data_type = col.info.get("data_type")
        possible_values = col.info.get("possible_values")
        if not data_type:
            data_type = SQLALCHEMY_TYPES_TO_DATA_TYPE.get(col.type.__visit_name__)
        if data_type == CATEGORIZED_DATA_TYPE and not possible_values:
            possible_values = [v[0] for v in db.query(distinct(col)).all()]
        columns.append(ColumnDefinition(column=col, type=data_type, possible_values=possible_values))
    db.close()
    return columns
