from pydantic import BaseModel, EmailStr, SecretStr, Field


class RefreshToken(BaseModel):
    """Refresh Token Schema"""
    refresh_token: str


class Token(RefreshToken):
    """Token Schema"""
    access_token: str
    refresh_token: str
    token_type: str


class TokenData(BaseModel):
    """Token Data Schema"""
    user_id: int


class UserRegister(BaseModel):
    """User Register Model"""
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password1: SecretStr = Field(repr=False)
    password2: SecretStr = Field(repr=False)


class User(BaseModel):
    """User Model"""
    first_name: str
    last_name: str
    email: EmailStr
    username: str


class UserLogin(BaseModel):
    """User Login Model"""
    email: EmailStr
    password: SecretStr
