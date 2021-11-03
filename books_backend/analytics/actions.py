from analytics import COLUMN_LISTS


def get_all_possible_columns_for_query():
    result = []
    for col in COLUMN_LISTS:
        result.append(col.to_pydantic_mode())
    return result