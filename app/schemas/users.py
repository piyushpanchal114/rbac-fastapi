from datetime import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """Schema for User"""
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    role: str
    created_at: datetime
    updated_at: datetime
