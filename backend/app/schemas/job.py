import uuid
from datetime import date, datetime

from pydantic import BaseModel, HttpUrl


class JobBase(BaseModel):
    title: str
    department: str | None = None
    company: str | None = None
    category: str | None = None
    sub_category: str | None = None
    location: list[str] | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    salary_text: str | None = None
    qualification: list[str] | None = None
    min_age: int | None = None
    max_age: int | None = None
    vacancies: int | None = None
    notification_date: date | None = None
    application_start: date | None = None
    application_end: date | None = None
    exam_date: date | None = None
    official_url: str
    source: str | None = None


class JobResponse(JobBase):
    job_id: uuid.UUID
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class JobListResponse(BaseModel):
    jobs: list[JobResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
