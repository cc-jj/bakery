from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from src import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(username: str) -> str:
    to_encode = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_TIMEOUT_MINUTES),
    }
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)


def decode_username(token: str) -> Optional[str]:
    payload = jwt.decode(
        token,
        settings.JWT_SECRET,
        settings.JWT_ALGO,
        options={"require_exp": True},
    )
    return payload["sub"]
