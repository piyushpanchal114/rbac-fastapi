from typing import Annotated
from fastapi import Depends, HTTPException, status
from models.db_models import User
from .dependancy import get_current_user


class RoleChecker:
    """Class for checking user roles"""

    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, user: Annotated[User, Depends(get_current_user)]):
        if user.role in self.allowed_roles:
            return True
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="You don't have enough permissions")
