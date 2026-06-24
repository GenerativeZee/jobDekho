import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    phone: str | None = None
    email: EmailStr | None = None
    name: str | None = None


class UserProfileUpdate(BaseModel):
    name: str | None = None
    age: int | None = None
    gender: str | None = None
    city: str | None = None
    state: str | None = None
    education_level: str | None = None
    field_of_study: str | None = None
    skills: list[str] | None = None
    experience_years: int | None = None
    job_type_pref: list[str] | None = None
    location_pref: list[str] | None = None
    sector_pref: list[str] | None = None
    salary_min_exp: int | None = None


class UserResponse(BaseModel):
    id: uuid.UUID
    phone: str | None = None
    email: str | None = None
    name: str | None = None
    age: int | None = None
    gender: str | None = None
    city: str | None = None
    state: str | None = None
    education_level: str | None = None
    field_of_study: str | None = None
    skills: list[str] | None = None
    experience_years: int = 0
    job_type_pref: list[str] | None = None
    location_pref: list[str] | None = None
    sector_pref: list[str] | None = None
    salary_min_exp: int | None = None
    is_verified: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
