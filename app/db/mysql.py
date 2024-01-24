import logging

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


class SQLAlchemy:
    def __init__(self, app: FastAPI = None, settings: settings = None):
        self._engine = None
        self._session = None
        if app is not None:
            self.init_app(app=app, settings=settings)

    def init_app(self, app: FastAPI = None, settings: settings = None):
        self._engine = create_engine(
            settings.DB_URL,
            pool_size=settings.DB_POOL_SIZE,
            max_overflow=settings.DB_POOL_MAX,
            pool_recycle=settings.DB_POOL_RECYCLE,
            pool_timeout=settings.DB_POOL_TIMEOUT,
            pool_pre_ping=True, )

        # expire_on_commit=False -> Because of sqlalchemy.orm.exc.DetachedInstanceError
        self._session = sessionmaker(autocommit=False, autoflush=False, bind=self._engine, expire_on_commit=False)

        if app:
            @app.on_event("startup")
            def startup():
                self._engine.connect()
                logging.info("DB connected.")

            @app.on_event("shutdown")
            def shutdown():
                self._session.close_all()
                self._engine.dispose()
                logging.info("DB disconnected")

    def get_db(self):
        if self._session is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()

    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine


db = SQLAlchemy()
Base = declarative_base()
