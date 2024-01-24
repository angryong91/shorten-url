from redis import Redis, from_url

from app.core.config import Settings

import logging

from fastapi import FastAPI


class RedisClient:
    def __init__(self) -> None:
        self.client: Redis = None

    def init_app(self, app: FastAPI = None, settings: Settings = None):
        if app:
            @app.on_event("startup")
            def startup():
                self.client = from_url(url=settings.REDIS_URL, decode_responses=True)
                logging.info("redis connected")

            @app.on_event("shutdown")
            def shutdown():
                self.client.close()
                logging.info("redis disconnected")


redis = RedisClient()
