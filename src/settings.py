import os

JWT_SECRET = os.environ["JWT_SECRET"]
JWT_ALGO = "HS256"
JWT_TIMEOUT_MINUTES = int(os.getenv("JWT_TIMEOUT_MINUTES", 60))

PORT = 8000

ENV = "dev"

SQLALCHEMY_DATABASE_URL = os.environ["SQLALCHEMY_DATABASE_URL"]


def dump():
    return {
        "ENV": ENV,
        "PORT": PORT,
        "JWT_TIMEOUT_MINUTES": JWT_TIMEOUT_MINUTES,
    }
