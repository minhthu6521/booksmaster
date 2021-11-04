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


@app.on_event("startup")
def create_query_builder():
    db = SessionLocal()
    _builder = DataQueryBuilder(db=db)
    db.close()
    return _builder


query_builder = create_query_builder()

import views

_used = views
