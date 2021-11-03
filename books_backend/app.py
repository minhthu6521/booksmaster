from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import distinct
from sqlalchemy import inspect

from analytics import CATEGORIZED_DATA_TYPE
from analytics import COLUMN_LISTS
from analytics import MODELS
from analytics import SQLALCHEMY_TYPES_TO_DATA_TYPE
from analytics.models import ColumnDefinition
from analytics.models import PossibleValue
from database import SessionLocal

app = FastAPI()

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def list_columns(db):
    for cls in MODELS:
        inst = inspect(cls)
        for col in inst.mapper.columns:
            data_type = col.info.get("data_type")
            possible_values = col.info.get("possible_values")
            if not data_type:
                data_type = SQLALCHEMY_TYPES_TO_DATA_TYPE.get(col.type.__visit_name__)
            if data_type == CATEGORIZED_DATA_TYPE and not possible_values:
                possible_values = [PossibleValue(label=v[0], value=v[0]) for v in db.query(distinct(col)).all()]
            COLUMN_LISTS.append(ColumnDefinition(column=col, type=data_type, possible_values=possible_values))


@app.on_event("startup")
def list_of_columns_in_class():
    db = SessionLocal()
    list_columns(db)
    db.close()
    return COLUMN_LISTS


import views

_used = views
