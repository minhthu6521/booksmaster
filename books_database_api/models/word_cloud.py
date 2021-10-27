from typing import List

from pydantic import BaseModel


class WordFrequency(BaseModel):
    text: str
    value: int
    occurrence: int


class WordCloud(BaseModel):
    words: List[WordFrequency]
