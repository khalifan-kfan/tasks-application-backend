from fastapi import FastAPI
from app import routes


def create_app() -> FastAPI:
    app = FastAPI()

    app.include_router(routes.router, prefix="/api")

    return app


app = create_app()
