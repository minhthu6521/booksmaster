from typing import Optional

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from actions.books_content_actions import get_word_cloud_of_book_content
from models.word_cloud import WordCloud

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
def get_word_cloud_from_book_content(book_id: int):
    result = get_word_cloud_of_book_content(book_id)
    return result