from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    """Verify hashed password"""
    return pwd_context.verify(plain_password, hashed_password)


def create_password_hash(password) -> str:
    """Function for creating hash password"""
    return pwd_context.hash(password)
