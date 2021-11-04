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
    MODELS.append(cls)
    return cls


