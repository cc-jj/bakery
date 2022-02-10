import logging
import sys
import traceback

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination
from sqlalchemy.exc import IntegrityError

from src import crud, routes, settings

logger = logging.getLogger("bakery")

app = FastAPI()


@app.on_event("startup")
def startup():
    logging.basicConfig(level=logging.INFO)
    if logger.isEnabledFor(logging.INFO):
        pretty_settings = (f"{k.lower():<25} {v}" for k, v in sorted(settings.dump().items()))
        logger.info("Settings\n%s", "\n".join(pretty_settings))


@app.exception_handler(IntegrityError)
def handle_integrity_error(request: Request, exc: IntegrityError):
    """Convert DB UniqueConstraint failures to 400 BadRequest failures"""
    if error_msg := crud.create_unique_constrain_error_msg(exc):
        return JSONResponse({"detail": error_msg}, 400)


async def catch_exceptions_middleware(request: Request, call_next):
    """
    Ensure CORS headers are added to response when an unhandled exception occurs:
    https://github.com/tiangolo/fastapi/issues/775#issuecomment-592946834
    """
    try:
        return await call_next(request)
    except Exception:
        logger.exception("Unhandled exception")
        content = {"detail": "Internal server error"}
        if settings.ENV == "dev":
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.format_exception(exc_type, exc_value, exc_traceback, limit=25)
            content.update(traceback=tb)
        return JSONResponse(content, status_code=500)


app.middleware("http")(catch_exceptions_middleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["Authorization"],
    allow_credentials=True,
)
app.include_router(routes.auth.router, prefix="/api")
app.include_router(routes.v1.router, prefix="/api")
add_pagination(app)
