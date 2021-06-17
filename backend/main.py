import logging

from fastapi import FastAPI
from fastapi.logger import logger as fastapi_logger
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

import routers
from routers.internal import admin
from core.config import settings

if "gunicorn" in str(settings.SERVER_SOFTWARE):
    """
    When running with gunicorn the log handlers get suppressed instead of
    passed along to the container manager. This forces the gunicorn handlers
    to be used throughout the project.
    """

    gunicorn_logger = logging.getLogger("gunicorn")
    log_level = gunicorn_logger.level

    root_logger = logging.getLogger()
    gunicorn_error_logger = logging.getLogger("gunicorn.error")
    uvicorn_access_logger = logging.getLogger("uvicorn.access")

    # Use gunicorn error handlers for root, uvicorn, and fastapi loggers
    root_logger.handlers = gunicorn_error_logger.handlers
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
    fastapi_logger.handlers = gunicorn_error_logger.handlers

    # Pass on logging levels for root, uvicorn, and fastapi loggers
    root_logger.setLevel(log_level)
    uvicorn_access_logger.setLevel(log_level)
    fastapi_logger.setLevel(log_level)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PATH}/openapi.json",
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["root"])
def root():
    return {"message": "Hello, Streamlit!"}


app.include_router(routers.api_router, prefix=settings.API_PATH)
app.include_router(admin.router, prefix=settings.API_PATH)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, debug=True)
