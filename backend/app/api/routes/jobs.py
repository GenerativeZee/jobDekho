import math
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.job import Job
from app.schemas.job import JobListResponse, JobResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])

CATEGORIES = [
    "banking", "railway", "ssc", "defence", "psc",
    "upsc", "engineering", "teaching", "police", "health"
]


@router.get("", response_model=JobListResponse)
async def list_jobs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: str | None = Query(None),
    location: str | None = Query(None),
    qualification: str | None = Query(None),
    q: str | None = Query(None, description="Search query"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Job).where(Job.is_active == True)

    if category:
        stmt = stmt.where(Job.category == category.lower())

    if location:
        stmt = stmt.where(Job.location.any(location))

    if qualification:
        stmt = stmt.where(Job.qualification.any(qualification))

    if q:
        search = f"%{q}%"
        stmt = stmt.where(
            or_(
                Job.title.ilike(search),
                Job.department.ilike(search),
                Job.company.ilike(search),
            )
        )

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = await db.scalar(count_stmt)

    stmt = (
        stmt.order_by(Job.application_end.asc().nulls_last(), Job.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )

    result = await db.execute(stmt)
    jobs = result.scalars().all()

    return JobListResponse(
        jobs=jobs,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=math.ceil(total / page_size) if total else 0,
    )


@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    counts = []
    for cat in CATEGORIES:
        stmt = select(func.count(Job.job_id)).where(
            Job.category == cat, Job.is_active == True
        )
        count = await db.scalar(stmt)
        if count:
            counts.append({"category": cat, "count": count})
    return counts


@router.get("/{job_id}", response_model=JobResponse)
async def get_job(job_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Job).where(Job.job_id == job_id, Job.is_active == True)
    )
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
