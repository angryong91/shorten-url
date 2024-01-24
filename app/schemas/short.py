from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey
)

from app.db.mysql import Base
from app.schemas.base import BaseMixin


class Shorts(Base, BaseMixin):
    __tablename__ = "shorts"
    id = Column(String(length=36), primary_key=True)
    origin_url = Column(String(length=2048), nullable=False)


class ShortClicks(Base, BaseMixin):
    __tablename__ = "short_clicks"
    id = Column(String(length=36), primary_key=True, default=lambda: str(uuid4()))
    short_id = Column(String(length=36), ForeignKey('shorts.id', ondelete='CASCADE'), index=True)
    click_count = Column(Integer, default=0)
