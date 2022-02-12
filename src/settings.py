import os

COOKIE_SECRET = os.environ["COOKIE_SECRET"]
COOKIE_MAX_AGE_MINUTES = int(os.environ["COOKIE_MAX_AGE_MINUTES"])

PORT = 8000

ENV = "dev"

SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]


def dump():
    return {
        "ENV": ENV,
        "PORT": PORT,
        "COOKIE_MAX_AGE_MINUTES": COOKIE_MAX_AGE_MINUTES,
    }
