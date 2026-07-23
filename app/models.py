"""SQLAlchemy ORM model(s) — this is your urls table definition: id, original_url, slug, created_at, expires_at, click_count. 
This defines the actual database schema, separate from what the API exposes."""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String,DateTime, func
from datetime import datetime

class Base(DeclarativeBase):
    pass


class URL(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    original_url: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    expires_at: Mapped[datetime | None] = mapped_column( DateTime(timezone=True), nullable=True)
    click_count: Mapped[int] = mapped_column(Integer, default=0)

