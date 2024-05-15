from fastapi import FastAPI

from saur.app.fastapi import db_lifespan

from .auth import auth_router
from .routes import notes_router


def create_app() -> FastAPI:
    app = FastAPI(lifespan=db_lifespan)

    app.include_router(auth_router)
    app.include_router(notes_router)

    return app
