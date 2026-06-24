"""
Cleanup script — removes junk scraped entries (nav links, reports, etc.)
and re-runs all crawlers with the fixed filters.

Run from backend/:
    python cleanup_jobs.py
"""
import asyncio
import logging
import re

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.job import Job

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)

# Sources whose live-scraped entries contained junk — we'll wipe and re-crawl them
DIRTY_SOURCES = {"ibps", "rrb", "upsc"}

# Titles that are definitely not job postings (from seed / old data)
JUNK_TITLE_PATTERNS = [
    r"statistical statement",
    r"annual report",
    r"former chairman",
    r"social responsib",
    r"personnel selection service",
    r"^recruitment exams?$",
    r"^examination$",
    r"^calendar$",
    r"^recruitment$",
    r"^active examination",
    r"^forthcoming examination",
    r"status of.*recruitment case",
    r"status of.*lateral",
    r"online recruitment application.*ora",
    r"eop for pwd",
    r"pratibha setu",
    r"representation on question",
]

_JUNK_RE = re.compile("|".join(JUNK_TITLE_PATTERNS), re.I)


async def cleanup(db: AsyncSession) -> int:
    result = await db.execute(select(Job).where(Job.source.in_(DIRTY_SOURCES)))
    jobs = result.scalars().all()

    to_delete = []
    for job in jobs:
        # Delete if title has no year (nav/section links never have years)
        has_year = bool(re.search(r"20\d\d", job.title or ""))
        is_junk_title = bool(_JUNK_RE.search(job.title or ""))
        if not has_year or is_junk_title:
            to_delete.append(job.job_id)
            logger.info(f"  Deleting: {job.title[:80]}")

    if to_delete:
        await db.execute(delete(Job).where(Job.job_id.in_(to_delete)))
        await db.commit()

    logger.info(f"Deleted {len(to_delete)} junk entries from sources {DIRTY_SOURCES}")
    return len(to_delete)


async def main():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    factory = async_sessionmaker(engine, expire_on_commit=False)

    async with factory() as db:
        deleted = await cleanup(db)

    logger.info(f"\nCleanup done — removed {deleted} junk entries.")
    logger.info("Now re-run crawlers:  python -m crawlers.runner all")


if __name__ == "__main__":
    asyncio.run(main())
