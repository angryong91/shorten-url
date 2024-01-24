import uvicorn

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.middleware.logger_middleware import LoggerMiddleware
from app.routes import api_router
from app.core.config import settings
from app.db.mysql import db
from app.db.redis import redis


def create_app():
    app = FastAPI(
            title=settings.PROJECT_NAME,
            description=settings.PROJECT_NAME,
            docs_url=f"/swagger",
            redoc_url=f"/redoc",
            debug=True
    )

    # init database
    db.init_app(app, settings)

    # set redis conn
    redis.init_app(app, settings)

    # set middleware
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        # allow_openapi=False,
        # allow_swagger_ui=True,
    )
    app.add_middleware(LoggerMiddleware)

    # set routes
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)