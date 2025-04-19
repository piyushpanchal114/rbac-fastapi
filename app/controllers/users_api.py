from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from schemas import users
from models.db_models import User
from models.enums import UserRoleEnum
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
