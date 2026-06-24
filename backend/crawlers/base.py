import hashlib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job import Job

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


@dataclass
class RawJob:
    """Parsed job data before DB write."""
    title: str
    official_url: str
    source: str
    department: str | None = None
    company: str | None = None
    category: str | None = None
    location: list[str] = field(default_factory=lambda: ["All India"])
    salary_text: str | None = None
    salary_min: int | None = None
    salary_max: int | None = None
    qualification: list[str] = field(default_factory=list)
    min_age: int | None = None
    max_age: int | None = None
    vacancies: int | None = None
    application_start: date | None = None
    application_end: date | None = None
    notification_date: date | None = None
    exam_date: date | None = None


@dataclass
class CrawlResult:
    source: str
    found: int = 0
    new: int = 0
    updated: int = 0
    skipped: int = 0
    errors: int = 0


class BaseCrawler(ABC):
    source: str = ""
    base_url: str = ""
    category: str = ""

    async def fetch(self, url: str, timeout: int = 20) -> str | None:
        """Fetch a URL with retry logic (3 attempts)."""
        for attempt in range(1, 4):
            try:
                async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=timeout) as client:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    return resp.text
            except httpx.HTTPStatusError as e:
                logger.warning(f"[{self.source}] HTTP {e.response.status_code} on {url} (attempt {attempt})")
            except Exception as e:
                logger.warning(f"[{self.source}] Error fetching {url} (attempt {attempt}): {e}")
        return None

    @abstractmethod
    async def crawl(self) -> list[RawJob]:
        """Fetch and parse jobs from the source. Return list of RawJob."""
        ...

    def make_hash(self, job: RawJob) -> str:
        key = f"{job.title}|{job.source}|{str(job.application_end)}"
        return hashlib.sha256(key.encode()).hexdigest()

    async def save(self, jobs: list[RawJob], db: AsyncSession) -> CrawlResult:
        result = CrawlResult(source=self.source, found=len(jobs))

        for raw in jobs:
            content_hash = self.make_hash(raw)
            try:
                existing = await db.scalar(
                    select(Job).where(Job.content_hash == content_hash)
                )

                if existing:
                    # Update vacancies/salary if changed
                    changed = False
                    if raw.vacancies and existing.vacancies != raw.vacancies:
                        existing.vacancies = raw.vacancies
                        changed = True
                    if raw.salary_text and existing.salary_text != raw.salary_text:
                        existing.salary_text = raw.salary_text
                        changed = True
                    if changed:
                        result.updated += 1
                    else:
                        result.skipped += 1
                else:
                    job = Job(
                        title=raw.title,
                        department=raw.department,
                        company=raw.company,
                        category=raw.category or self.category,
                        location=raw.location,
                        salary_text=raw.salary_text,
                        salary_min=raw.salary_min,
                        salary_max=raw.salary_max,
                        qualification=raw.qualification,
                        min_age=raw.min_age,
                        max_age=raw.max_age,
                        vacancies=raw.vacancies,
                        application_start=raw.application_start,
                        application_end=raw.application_end,
                        notification_date=raw.notification_date,
                        exam_date=raw.exam_date,
                        official_url=raw.official_url,
                        source=raw.source or self.source,
                        content_hash=content_hash,
                        is_active=True,
                    )
                    db.add(job)
                    result.new += 1

            except Exception as e:
                logger.error(f"[{self.source}] Failed to save '{raw.title}': {e}")
                result.errors += 1

        await db.commit()
        return result

    async def run(self, db: AsyncSession) -> CrawlResult:
        logger.info(f"[{self.source}] Starting crawl → {self.base_url}")
        try:
            jobs = await self.crawl()
        except Exception as e:
            logger.error(f"[{self.source}] Crawl failed: {e}")
            return CrawlResult(source=self.source, errors=1)

        result = await self.save(jobs, db)
        logger.info(
            f"[{self.source}] Done — found={result.found} new={result.new} "
            f"updated={result.updated} skipped={result.skipped} errors={result.errors}"
        )
        return result
