from datetime import datetime
from sqlalchemy import orm


class Base(orm.DeclarativeBase):
    pass


class User(Base):
    """User Model"""
    __tablename__ = "user"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    first_name: orm.Mapped[str]
    last_name: orm.Mapped[str]
    username: orm.Mapped[str] = orm.mapped_column(unique=True, nullable=False)
    email: orm.Mapped[str] = orm.mapped_column(unique=True, nullable=False)
    password: orm.Mapped[str] = orm.mapped_column(nullable=False)
    role: orm.Mapped[str] = orm.mapped_column(
        nullable=False, enumerated=["user", "admin"], default="user")

    contacts: orm.Mapped[list["Contact"]] = orm.relationship(
        "Contact", back_populates="owner")


class Contact(Base):
    """Contact Model"""
    __tablename__ = "contact"
    id: orm.Mapped[int] = orm.mapped_column(primary_key=True, index=True)
    user_id: orm.Mapped[int] = orm.mapped_column(orm.ForeignKey("user.id"))
    name: orm.Mapped[str] = orm.mapped_column(nullable=False)
    phone: orm.Mapped[str]
    email: orm.Mapped[str]
    notes: orm.Mapped[str]
    created_at: orm.Mapped[datetime] = orm.mapped_column(default=datetime.now)
    updated_at: orm.Mapped[datetime] = orm.mapped_column(
        default=datetime.now, onupdate=datetime.now)

    owner: orm.Mapped[User] = orm.relationship(
        "User", back_populates="contacts")
