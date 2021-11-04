from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from query_builder.main import DataQueryBuilder
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
query_builder = None


@app.on_event("startup")
def list_of_columns_in_class():
    global query_builder
    db = SessionLocal()
    _builder = DataQueryBuilder(db=db)
    db.close()
    query_builder = _builder


import views

_used = views
