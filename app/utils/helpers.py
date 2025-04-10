from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.db_models import User


async def get_user(user_id: int, db: AsyncSession) -> User | None:
    """Function for getting user by id"""
    qs = await db.scalars(select(User).where(User.id == user_id))
    return qs.first()
