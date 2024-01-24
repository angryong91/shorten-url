from datetime import datetime

from pydantic import Field, HttpUrl

from app.models.base import CamelModel


class ShortCreate(CamelModel):
    url: HttpUrl = Field(example="https://airbridge.io")


class ShortInfo(CamelModel):
    short_id: str = Field(example="abcde", min_length=3)
    url: HttpUrl = Field(example="https://airbridge.io")
    created_at: datetime = Field(example="2024-01-24 16:46:33")

    # class Config:
    #     from_attributes = True
