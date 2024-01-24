import hashlib
from typing import Union
from uuid import uuid4

import base62

from app.db.redis import redis
from app.schemas.short import Shorts, ShortClicks


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
            ShortClicks.create(short_id=short.id)
            set_cache_url(short.id, origin_url)
            return short


def get_short(short_id: str) -> Shorts:
    return Shorts.get(id=short_id)


def get_cache_url(short_id: str) -> str:
    return redis.client.get(short_id)


def set_cache_url(short_id: str, origin_url: str, expire_time: int = 3600) -> bool:
    return redis.client.set(short_id, str(origin_url), expire_time)

def update_short_click(short_id: str):
    short_click = ShortClicks.get(short_id=short_id)
    ShortClicks.filter(short_id=short_id).update(click_count=short_click.click_count + 1)


def shorten_url(url: str) -> str:
    md5_hash = hashlib.md5(f"{url}{uuid4()}".encode()).hexdigest()
    return base62.encode(int(md5_hash, 16))
