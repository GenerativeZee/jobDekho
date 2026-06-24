import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    phone: Mapped[str | None] = mapped_column(String(15), unique=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True)
    name: Mapped[str | None] = mapped_column(String(200))
    age: Mapped[int | None] = mapped_column(Integer)
    gender: Mapped[str | None] = mapped_column(String(20))
    city: Mapped[str | None] = mapped_column(String(100))
    state: Mapped[str | None] = mapped_column(String(100))
    education_level: Mapped[str | None] = mapped_column(String(50))
    field_of_study: Mapped[str | None] = mapped_column(String(100))
    skills: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    experience_years: Mapped[int] = mapped_column(Integer, default=0)
    job_type_pref: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    location_pref: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    sector_pref: Mapped[list[str] | None] = mapped_column(ARRAY(Text))
    salary_min_exp: Mapped[int | None] = mapped_column(Integer)
    hashed_password: Mapped[str | None] = mapped_column(Text)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
