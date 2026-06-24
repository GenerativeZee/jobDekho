"""Second-pass cleanup — removes leftover seed duplicates and remaining junk."""
import asyncio
from sqlalchemy import delete, or_
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.config import settings
from app.models.job import Job

# Exact stale seed titles that have duplicates with better URLs from crawlers
STALE_SEED_TITLES = {
    "UPSC Civil Services 2026",
    "IBPS PO 2026",
    "IBPS Clerk 2026",
    "Railway Group D 2026",
    "RRB NTPC Graduate Level 2026",
}

# Known junk documents that slipped through
JUNK_URL_PATTERNS = [
    "Statistical",
    "Vacancy_Circular",
    "instructions-candidates-qualified",
]


async def main():
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    factory = async_sessionmaker(engine, expire_on_commit=False)

    async with factory() as db:
        # Delete stale seed duplicates
        r1 = await db.execute(
            delete(Job).where(Job.title.in_(STALE_SEED_TITLES))
        )
        # Delete junk documents by URL substring
        for pattern in JUNK_URL_PATTERNS:
            await db.execute(
                delete(Job).where(Job.official_url.contains(pattern))
            )
        # Delete any remaining entries whose title contains junk patterns
        await db.execute(
            delete(Job).where(
                or_(
                    Job.title.ilike("%Statistical Instruction%"),
                    Job.title.ilike("%Vacancy_Circular%"),
                    Job.title.ilike("%instructions for the candidates qualified%"),
                )
            )
        )
        await db.commit()
        print(f"Removed {r1.rowcount} stale seed entries + junk documents.")
        print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
