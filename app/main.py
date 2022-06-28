import logging

import sentry_sdk
from api.endpoints import categories, develop, jobs, login, tasks, users
from core.config import get_settings
from core.logger import get_logger, init_gunicorn_uvicorn_logger
from fastapi import FastAPI
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from starlette.middleware.cors import CORSMiddleware

logger = get_logger(__name__)
settings = get_settings()
init_gunicorn_uvicorn_logger(settings.LOGGER_CONFIG_PATH)

sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.ERROR)

app = FastAPI(title=f"[{settings.ENV}]{settings.TITLE}", version=settings.VERSION)

if settings.SENTRY_SDK_DNS:
    sentry_sdk.init(  # type: ignore
        dsn=settings.SENTRY_SDK_DNS,
        integrations=[sentry_logging, SqlalchemyIntegration()],
        environment=settings.ENV,
    )


app.add_middleware(SentryAsgiMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
    allow_origin_regex=r"^https?:\/\/([\w\-\_]{1,}\.|)example\.com",
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.add_exception_handler(Exception, http_exception_handler)


@app.get("/", tags=["info"])
def get_info() -> dict:
    return {"title": settings.TITLE, "version": settings.VERSION}


app.include_router(login.router, tags=["ログイン"], prefix="/login")
app.include_router(users.router, tags=["Users(ユーザーアカウント)"], prefix="/users")
app.include_router(jobs.router, tags=["Jobs(求人)"], prefix="/jobs")
app.include_router(categories.router, tags=["Categories(カテゴリー)"], prefix="/categories")
app.include_router(tasks.router, tags=["Tasks"], prefix="/tasks")
app.include_router(develop.router, tags=["Develop"], prefix="/develop")
