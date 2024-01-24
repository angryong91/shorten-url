from datetime import datetime, UTC
from typing import Union

from app.db.mongo import mongodb
from app.db.redis import get_client
from app.schemas.short import Shorts
from app.utils.date import datetime_range
from app.utils.hash import shorten_url


def create_short(origin_url: str) -> Union[None, Shorts]:
    hash_url = shorten_url(origin_url)
    count = 3
    while True:
        if count > 10:
            return None

        if get_short(hash_url[:count]):
            count += 1
        else:
            short = Shorts.create(id=hash_url[:count], origin_url=origin_url)
            set_cache_url(short.id, origin_url)
            return short


def get_short(short_id: str) -> Shorts:
    return Shorts.get(id=short_id)


def get_cache_url(short_id: str) -> str:
    redis = get_client()
    return redis.get(short_id)


def set_cache_url(short_id: str, origin_url: str, expire_time: int = 3600) -> bool:
    redis = get_client()
    return redis.set(short_id, str(origin_url), expire_time)


def del_cache_url(short_id: str) -> bool:
    redis = get_client()
    return redis.delete(short_id)


async def create_short_click(short_id: str):
    short_click = dict(short_id=short_id, created_at=datetime.now(UTC))
    await mongodb.collection.insert_one(short_click)


async def count_short_click(short_id: str) -> list[dict[str, int]]:
    date_list = datetime_range()
    result = []
    for i in range(len(date_list) - 1):
        date_dict = dict()
        start_date = date_list[i]
        end_date = date_list[i + 1]
        date_dict["time"] = end_date
        date_dict["count"] = await mongodb.collection.count_documents(
            {"short_id": short_id, "created_at": {"$gte": start_date, "$lt": end_date}})
        result.append(date_dict)

    return result
