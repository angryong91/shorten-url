from sqlalchemy import (
    Column,
    String
)

from app.db.mysql import Base
from app.schemas.base import BaseMixin


class Shorts(Base, BaseMixin):
    __tablename__ = "shorts"
    id = Column(String(length=36), primary_key=True)
    origin_url = Column(String(length=2048), nullable=False)
