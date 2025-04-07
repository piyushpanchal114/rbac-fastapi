import jwt
from datetime import datetime, timedelta, timezone
from config import settings


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Function for creating access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret,
                             algorithm=settings.algorithm)
    return encoded_jwt
