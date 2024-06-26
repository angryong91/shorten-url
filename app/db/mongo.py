from app.core.config import Settings
from app.utils.logger import logger
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDB:
    def __init__(self):
        self.client = None
        self.database = None
        self.collection = None

    def init_app(self, app: FastAPI = None, settings: Settings = None):
        if app:
            @app.on_event("startup")
            async def on_app_start():
                self.client = AsyncIOMotorClient(settings.MONGO_DB_URL)
                self.database = self.client.get_database("short_clicks")
                self.collection = self.database.get_collection("short_clicks_collection")

                existing_indexes = await self.collection.index_information()

                if "short_id_1" not in existing_indexes:
                    await self.collection.create_index([("short_id", 1)])
                if "created_at_1" not in existing_indexes:
                    await self.collection.create_index([("created_at", 1)])

                logger.info("mongo connected.")

            @app.on_event("shutdown")
            async def on_app_shutdown():
                self.client.close()
                logger.info("mongo disconnected.")


mongodb = MongoDB()
