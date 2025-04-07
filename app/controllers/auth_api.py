from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from models.db_models import User
from schemas import auth
from utils.hashers import create_password_hash


router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}})


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    data: auth.UserRegister,
        session: AsyncSession = Depends(get_session)) -> auth.User:
    """Function for registering new user"""
    user_details = data.model_dump()
    if user_details["password1"] != user_details["password2"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail={"detial": "Password mismatched"})
    result = await session.scalars(
            select(User).filter(
                or_(User.username == user_details["username"],
                    User.email == user_details["email"])))
    if result.first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"detail": "username or email already exists"})
    password = user_details["password1"]
    hashed_password = create_password_hash(password.get_secret_value())
    new_user = User(first_name=user_details["first_name"],
                    last_name=user_details["last_name"],
                    email=user_details["email"],
                    username=user_details["username"],
                    password=hashed_password)
    session.add(new_user)
    await session.commit()
    return user_details
