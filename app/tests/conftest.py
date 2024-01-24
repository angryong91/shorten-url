from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database
from starlette.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.schemas import Shorts
from app.services.short import set_cache_url, del_cache_url

TEST_DATABASE_URL = f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_SERVER}/test"
TEST_REDIS_URL = f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/test" \
    if settings.REDIS_PASSWORD else f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/test"
TestBase = declarative_base()


@pytest.fixture(scope="session")
def db_session() -> Generator:
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    test_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    if database_exists(engine.url):
        drop_database(engine.url)

    create_database(engine.url)
    try:
        from alembic.config import Config as AlembicConfig
        from alembic.command import upgrade as alembic_upgrade, downgrade as alembic_downgrade

        alembic_config = AlembicConfig(f"{settings.BASE_DIR}/alembic.ini")
        alembic_config.set_main_option('sqlalchemy.url', TEST_DATABASE_URL)
        alembic_config.set_main_option('script_location', f"{settings.BASE_DIR}/migrations")
        alembic_upgrade(alembic_config, 'head')
    except Exception as e:
        raise e

    db = test_session()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def app_client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def create_shorts(request):
    Shorts.create(id="3rc", origin_url="https://airbridge.io")

    def delete_shorts():
        Shorts.filter(id="3rc").delete()

    request.addfinalizer(delete_shorts)


@pytest.fixture
def caching_shorts(request):
    set_cache_url("3rc", "https://airbridge.io")

    def delete_cache():
        del_cache_url("3rc")

    request.addfinalizer(delete_cache)
