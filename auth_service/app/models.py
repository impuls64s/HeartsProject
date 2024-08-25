from __future__ import annotations

import asyncio
import datetime
import enum
from typing import List

from sqlalchemy import ForeignKey, String, Integer, Enum
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import selectinload


class Base(AsyncAttrs, DeclarativeBase):
    pass


class StatusEnum(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"
    BANNED = "BANNED"
    UNDER_REVIEW = "UNDER_REVIEW"
    PREMIUM = "PREMIUM"


class GenderEnum(enum.Enum):
    MAN = 'MAN'
    WOMAN = 'WOMAN'


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    password: Mapped[str] = mapped_column(String(70), nullable=False)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[GenderEnum]
    height: Mapped[int] = mapped_column(Integer, nullable=True)
    weight: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), nullable=False, default=StatusEnum.UNDER_REVIEW)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, status={self.status!r})"
