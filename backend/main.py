from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.auth import router as auth_router
from routers.users import router as user_router
from settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        docs_url=f"{settings.root_path}/docs",
        openapi_url=f"{settings.root_path}",
        version="0.1.0",
        title="API Template"
    )

    app.include_router(auth_router)
    app.include_router(user_router)

    origins = [
        "*",
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
