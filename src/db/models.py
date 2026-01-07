from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "Users"

    telegram_id: Mapped[int] = mapped_column(primary_key=True) 
    email: Mapped[str] = mapped_column(nullable=False)
    app_password: Mapped[str] = mapped_column(nullable=False) 