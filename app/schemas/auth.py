from pydantic import BaseModel, EmailStr, SecretStr, Field


class Token(BaseModel):
    """Token Schema"""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token Data Schema"""
    username: str


class UserRegister(BaseModel):
    """User Register Model"""
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password1: SecretStr = Field(repr=False)
    password2: SecretStr = Field(repr=False)
