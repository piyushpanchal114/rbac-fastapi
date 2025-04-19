from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from schemas import users
from models.db_models import User
from models.enums import UserRoleEnum
from utils.helpers import get_user
from utils.permissions import RoleChecker

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}})


@router.get("/")
async def get_all_users(
        _: Annotated[bool, Depends(
            RoleChecker(allowed_roles=[UserRoleEnum.admin]))],
        session: AsyncSession = Depends(get_session)) -> list[users.User]:
    """Get All Users"""
    users = await session.scalars(select(User).order_by(User.created_at))
    return users


@router.get("/{user_id}")
async def get_user_details(
     _: Annotated[bool, Depends(
         RoleChecker(allowed_roles=[UserRoleEnum.admin]))],
     user_id: int, session: AsyncSession = Depends(get_session)) -> users.User:
    user = await get_user(user_id=user_id, db=session)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User with user id does not exists.")
    return user
