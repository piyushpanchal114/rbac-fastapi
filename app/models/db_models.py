from datetime import datetime
from sqlalchemy import orm, Enum, ForeignKey, DateTime
from sqlalchemy.sql import func
from .enums import UserRoleEnum


class Base(orm.DeclarativeBase):
    """Base Model"""
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    created_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=func.now())
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        DateTime(timezone=True), default=func.now(), onupdate=func.now())


class User(Base):
    """User Model"""
    __tablename__ = "user"
    first_name: orm.Mapped[str]
    last_name: orm.Mapped[str]
    username: orm.Mapped[str] = orm.mapped_column(unique=True, nullable=False)
    email: orm.Mapped[str] = orm.mapped_column(unique=True, nullable=False)
    password: orm.Mapped[str] = orm.mapped_column(nullable=False)
    role: orm.Mapped[str] = orm.mapped_column(
        Enum(UserRoleEnum), nullable=False, default="user")

    contacts: orm.Mapped[list["Contact"]] = orm.relationship(
        "Contact", back_populates="owner")


class Contact(Base):
    """Contact Model"""
    __tablename__ = "contact"
    user_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("user.id"))
    name: orm.Mapped[str] = orm.mapped_column(nullable=False)
    phone: orm.Mapped[str]
    email: orm.Mapped[str]
    notes: orm.Mapped[str]

    owner: orm.Mapped[User] = orm.relationship(
        "User", back_populates="contacts")
