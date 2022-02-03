import logging
import sys
import traceback

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from src import routes, settings

logger = logging.getLogger("bakery")

app = FastAPI()


@app.on_event("startup")
def startup():
    logging.basicConfig(level=logging.INFO)
    if settings.DEBUG_MODE:
        logger.setLevel(logging.DEBUG)
    if logger.isEnabledFor(logging.INFO):
        pretty_settings = (f"{k.lower():<25} {v}" for k, v in sorted(settings.dump().items()))
        logger.info("Settings\n%s", "\n".join(pretty_settings))


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
        if settings.DEBUG_MODE:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            tb = traceback.format_exception(exc_type, exc_value, exc_traceback, limit=25)
            content.update(traceback=tb)
        return JSONResponse(content, status_code=500)


app.middleware("http")(catch_exceptions_middleware)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["Authorization"],
)
app.include_router(routes.auth.router, prefix="/api")
app.include_router(routes.v1.router, prefix="/api")
add_pagination(app)
