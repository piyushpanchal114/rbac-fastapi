import jwt
import uuid
from datetime import datetime, timedelta, timezone
from typing import Literal
from config import settings


def create_jwt_token(data: dict, type: Literal["refresh", "access"],
                     expires_delta: timedelta | None = None):
    """Function for creating jwt token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    elif type == "refresh":
        expire = datetime.now(timezone.utc) + timedelta(days=30)
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    created_at = datetime.now(timezone.utc)
    payload = {"token_type": type, "exp": expire,
               "iat": created_at, "jti": str(uuid.uuid4())}
    payload.update(**to_encode)
    encoded_jwt = jwt.encode(payload, settings.secret,
                             algorithm=settings.algorithm)
    return encoded_jwt
