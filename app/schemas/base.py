from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    DateTime,
    func,
    or_,
)
from sqlalchemy.orm import Session

from app.db.mysql import db


class BaseMixin:
    created_at = Column(DateTime, nullable=False, default=func.current_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.current_timestamp(), onupdate=func.current_timestamp())
    deleted_at = Column(DateTime, nullable=True)

    def __init__(self):
        self._q = None
        self._session = None
        self.served = None

    def all_columns(self):
        return [c for c in self.__table__.columns]

    def __hash__(self):
        return hash(self.id)

    @classmethod
    def create(cls, session: Session = None, **kwargs):
        session = next(db.session()) if not session else session
        obj = cls()
        for col in obj.all_columns():
            col_name = col.name
            if col_name in kwargs:
                setattr(obj, col_name, kwargs.get(col_name))
        session.add(obj)
        session.commit()
        session.refresh(obj)
        return obj

    @classmethod
    def get(cls, session: Session = None, **kwargs):
        session = next(db.session()) if not session else session
        query = session.query(cls)
        for key, val in kwargs.items():
            col = getattr(cls, key)
            query = query.filter(col == val)
        if query.count() > 1:
            raise Exception("Only one row is supposed to be returned, but got more than one.")

        return query.first()

    @classmethod
    def filter(cls, session: Session = None, **kwargs):
        cond = []
        for key, val in kwargs.items():
            key = key.split("__")
            col = getattr(cls, key[0])
            if len(key) == 1:
                cond.append((col == val))
            elif len(key) == 2 and key[1] == 'not':
                cond.append((col != val))
            elif len(key) == 2 and key[1] == 'gt':
                cond.append((col > val))
            elif len(key) == 2 and key[1] == 'gte':
                cond.append((col >= val))
            elif len(key) == 2 and key[1] == 'lt':
                cond.append((col < val))
            elif len(key) == 2 and key[1] == 'lte':
                cond.append((col <= val))
            elif len(key) == 2 and key[1] == 'in':
                cond.append((col.in_(val)))
            elif len(key) == 2 and key[1] == 'like':
                cond.append((col.contains(val)))
            elif len(key) == 2 and key[1] == 'like_in':
                like_conds = [col.contains(v) for v in val]
                in_cond = col.in_(val)
                cond.append(or_(*like_conds, in_cond))
            elif len(key) == 2 and key[1] == 'all':
                cond.append((col.all_(val)))

        obj = cls()
        if session:
            obj._session = session
            obj.served = True
        else:
            obj._session = next(db.session())
            obj.served = False
        query = obj._session.query(cls)
        query = query.filter(*cond)
        obj._q = query
        return obj

    @classmethod
    def cls_attr(cls, col_name=None):
        if col_name:
            col = getattr(cls, col_name)
            return col
        else:
            return cls

    @classmethod
    def is_cls_attr(cls, col_name=None):
        try:
            getattr(cls, col_name)
        except:
            return False
        return True

    def update(self, **kwargs):
        remove_list = []
        for key in kwargs.keys():
            if not self.is_cls_attr(key):
                remove_list.append(key)
        for key in remove_list:
            kwargs.pop(key)
        query_set = self._q.update(kwargs)
        result = None

        if query_set > 0:
            result = self._q.first()

        self._session.commit()
        self._session.close()
        return result

    def delete(self):
        self._q.delete()
        self._session.commit()

    def close(self):
        if not self.served:
            self._session.close()
        else:
            self._session.flush()
