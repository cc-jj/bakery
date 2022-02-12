import logging
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, Request, Response
from passlib.context import CryptContext
from starlette.status import HTTP_403_FORBIDDEN

from src import settings

logger = logging.getLogger("bakery")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def set_cookie(response: Response, username: str):
    created_at = datetime.now(timezone.utc)
    expires_at = created_at + timedelta(minutes=settings.COOKIE_MAX_AGE_MINUTES)
    token = create_token(username, created_at, expires_at)
    response.set_cookie(
        "token",
        token,
        max_age=settings.COOKIE_MAX_AGE_MINUTES * 60,
        httponly=True,
        samesite="strict",
    )
    return response


def remove_cookie(response: Response):
    response.set_cookie("token", "", max_age=0)
    return response


def verify_cookie(request: Request) -> dict:
    token = request.cookies.get("token")
    if token is None:
        raise HTTPException(HTTP_403_FORBIDDEN, "Not authenticated")
    try:
        return decode_token(token)
    except jwt.PyJWTError:
        raise HTTPException(HTTP_403_FORBIDDEN, "Credentials invalid or expired")


def create_token(username: str, created_at: datetime, expires_at: datetime) -> str:
    logger.debug("create_token")
    payload = {
        "sub": username,
        "iat": created_at,
        "exp": expires_at,
    }
    return jwt.encode(payload, settings.COOKIE_SECRET, algorithm="HS256")


def decode_token(token: str) -> dict:
    logger.debug("decode_token")
    payload = jwt.decode(
        token,
        settings.COOKIE_SECRET,
        algorithms=["HS256"],
        options={"require": ["sub", "iat", "exp"]},
    )
    return {
        "username": payload["sub"],
        "created_at": datetime.fromtimestamp(payload["iat"], timezone.utc),
        "expires_at": datetime.fromtimestamp(payload["exp"], timezone.utc),
    }
