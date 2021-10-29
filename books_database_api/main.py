from typing import Optional

from aiocache import Cache
from aiocache import cached
from aiocache.serializers import JsonSerializer
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware

from actions.books_content_actions import get_word_cloud_of_book_content
from models.word_cloud import WordCloud
from redis_conf import REDIS_CONF

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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/books/{book_id}/contents/wordcloud", response_model=WordCloud)
@cached(**REDIS_CONF)
async def get_word_cloud_from_book_content(book_id: int, min: Optional[int] = 1, max: Optional[int] = None):
    result = get_word_cloud_of_book_content(book_id, min, max)
    return jsonable_encoder(result)

