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

EQUAL = "equal"
NOT_EQUAL = "not equal"
IN = "in"
NOT_IN = "not in"
FALSE = "false"
TRUE = "true"
NONE = "(empty)"
EMPTY_STRING = "(empty_string)"
LARGER = "larger"
SMALLER = "smaller"
AND = "and"
OR = "or"

CLAUSES = {
    EQUAL: lambda col, value: f"{col} == {value}",
    IN: lambda col, value: f"{col}.in_({value})",
    NOT_EQUAL: lambda col, value: f"{col} != {value}",
    NOT_IN: lambda col, value: f"{col}.notin_({value})",
    LARGER: lambda col, value: f"{col} > {value}",
    SMALLER: lambda col, value: f"{col} < {value}",
}

OPERATIONS = {
    AND: lambda clause: f"and_({str(*clause)})",
    OR: lambda clause: f"or_({str(*clause)})"
}

VALUES = {
    FALSE: False,
    TRUE: True,
    NONE: None,
    EMPTY_STRING: ""
}


def for_analytics(cls):
    MODELS.append(cls)
    return cls
