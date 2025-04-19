import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from config import settings
from db import get_session
from schemas.auth import TokenData
from .helpers import get_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme),
                           session: AsyncSession = Depends(get_session)):
    """Function for getting current user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.secret, settings.algorithm)
        user_id = payload.get("user_id")
        token_type = payload.get("token_type")
        if token_type != "access":
            raise credentials_exception
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = await get_user(user_id=token_data.user_id, db=session)
    if user is None:
        raise credentials_exception
    return user


async def validate_refresh_token(token: str, db: AsyncSession):
    """Function for validating refresh token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Token")
    try:
        payload = jwt.decode(token, settings.secret, settings.algorithm)
        token_type = payload.get("token_type")
        user_id = payload.get("user_id")
        if token_type != "refresh":
            raise credentials_exception
        if user_id is None:
            raise credentials_exception
        user = await get_user(user_id=user_id, db=db)
        if user is None:
            raise credentials_exception
        return user
    except jwt.InvalidTokenError:
        raise credentials_exception
