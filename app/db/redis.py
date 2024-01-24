from typing import Union

from app.core.config import settings
from redis import Redis, from_url

redis_client: Union[Redis, None] = None


def set_client(redis_url=settings.REDIS_URL) -> None:
    global redis_client
    redis_client = from_url(url=redis_url, decode_responses=True)


def get_client() -> Redis:
    global redis_client
    return redis_client


async def discard_client() -> None:
    global redis_client
    redis_client.close()
