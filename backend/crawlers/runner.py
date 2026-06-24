"""
Crawler runner.

Usage:
    python -m crawlers.runner ssc          # run one crawler
    python -m crawlers.runner all          # run every registered crawler
    python -m crawlers.runner ssc --dry    # parse only, no DB write
"""
import asyncio
import logging
import sys

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from crawlers.base import BaseCrawler, CrawlResult
from crawlers.ssc import SSCCrawler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# Registry: add new crawlers here as you build them
CRAWLERS: dict[str, type[BaseCrawler]] = {
    "ssc": SSCCrawler,
}


def _make_session() -> AsyncSession:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
    factory = async_sessionmaker(engine, expire_on_commit=False)
    return factory()


async def run_one(name: str, dry: bool = False) -> CrawlResult:
    cls = CRAWLERS.get(name)
    if not cls:
        logger.error(f"Unknown crawler: '{name}'. Available: {list(CRAWLERS)}")
        return CrawlResult(source=name, errors=1)

    crawler = cls()

    if dry:
        logger.info(f"[{name}] DRY RUN — fetching and parsing only, no DB write")
        jobs = await crawler.crawl()
        logger.info(f"[{name}] Would save {len(jobs)} jobs:")
        for j in jobs:
            logger.info(f"  • {j.title[:80]}  |  deadline={j.application_end}  |  vacancies={j.vacancies}")
        return CrawlResult(source=name, found=len(jobs))

    async with _make_session() as db:
        return await crawler.run(db)


async def run_all(dry: bool = False) -> list[CrawlResult]:
    results = []
    for name in CRAWLERS:
        result = await run_one(name, dry=dry)
        results.append(result)
    return results


async def main():
    args = sys.argv[1:]
    dry = "--dry" in args
    targets = [a for a in args if not a.startswith("--")]

    if not targets:
        print(f"Usage: python -m crawlers.runner <name|all> [--dry]")
        print(f"Available crawlers: {list(CRAWLERS)}")
        sys.exit(1)

    if targets[0] == "all":
        results = await run_all(dry=dry)
    else:
        results = [await run_one(targets[0], dry=dry)]

    print("\n-- Crawl Summary ------------------------------------------")
    for r in results:
        print(
            f"  {r.source:<12}  found={r.found}  new={r.new}  "
            f"updated={r.updated}  skipped={r.skipped}  errors={r.errors}"
        )
    print("------------------------------------------------------------")


if __name__ == "__main__":
    asyncio.run(main())
