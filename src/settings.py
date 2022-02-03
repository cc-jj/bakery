import os

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGO = "HS256"
JWT_TIMEOUT_MINUTES = int(os.getenv("JWT_TIMEOUT_MINUTES", 60))

# Controls logging level and enables including traceback in 500 InternalServerError responses
DEBUG_MODE = os.getenv("DEBUG") == "1"

SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]


def dump():
    return {
        "DEBUG_MODE": DEBUG_MODE,
        "JWT_TIMEOUT_MINUTES": JWT_TIMEOUT_MINUTES,
    }
