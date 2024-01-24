from datetime import datetime

from app.models.base import CamelModel
from pydantic import Field, HttpUrl


class ShortCreate(CamelModel):
    url: HttpUrl = Field(example="https://airbridge.io")


class ShortInfo(CamelModel):
    short_id: str = Field(example="abcde", min_length=3)
    url: HttpUrl = Field(example="https://airbridge.io")
    created_at: datetime = Field(example="2024-01-24T00:00:00+00:00")


class ShortCounts(CamelModel):
    time: datetime = Field(example="2024-01-24T00:00:00+00:00")
    count: int = Field(example=0)
