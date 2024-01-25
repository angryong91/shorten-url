from datetime import datetime

from app.exceptions import BadRequest
from app.models.base import CamelModel
from pydantic import Field, HttpUrl, field_validator


class ShortCreate(CamelModel):
    url: HttpUrl = Field(example="https://airbridge.io")


class ShortId(CamelModel):
    short_id: str = Field()

    @field_validator('short_id')
    def short_id_alphanumeric(cls, v):
        if not v.isalnum():
            raise BadRequest('short_id must be alphanumeric')
        return v


class ShortInfo(ShortId):
    short_id: str = Field(example="abcde", min_length=3)
    url: HttpUrl = Field(example="https://airbridge.io")
    created_at: datetime = Field(example="2024-01-24T00:00:00+00:00")


class ShortCounts(CamelModel):
    time: datetime = Field(example="2024-01-24T00:00:00+00:00")
    count: int = Field(example=0)
