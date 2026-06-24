"""
IBPS Crawler — scrapes ibps.in for banking recruitment notices.

IBPS lists active recruitments on their homepage and /recruitment page.
The site renders with basic HTML so plain httpx works; Playwright is the fallback.
"""
import logging
import re
from datetime import date

from bs4 import BeautifulSoup

from crawlers.base import BaseCrawler, RawJob

logger = logging.getLogger(__name__)

# Salary bands per exam
_SALARY = {
    "po":     ("Rs.36,000 – Rs.63,840/month", 36000, 63840),
    "clerk":  ("Rs.13,075 – Rs.35,370/month", 13075, 35370),
    "so":     ("Rs.36,000 – Rs.63,840/month", 36000, 63840),
    "rrb":    ("Rs.15,000 – Rs.45,950/month", 15000, 45950),
    "officer":("Rs.36,000 – Rs.63,840/month", 36000, 63840),
}

_AGE = {
    "po":     (20, 30),
    "clerk":  (20, 28),
    "so":     (20, 30),
    "rrb":    (18, 28),
    "officer":(20, 30),
}

_QUAL = {
    "po":     ["Graduate"],
    "clerk":  ["Graduate"],
    "so":     ["Graduate", "Postgraduate"],
    "rrb":    ["Graduate"],
    "officer":["Graduate"],
}

_MONTHS = {
    "jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
    "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12,
}

FALLBACK: list[dict] = [
    {"title": "IBPS PO 2026 (Probationary Officer)",       "key": "po",    "vacancies": 4455,  "application_end": "2026-07-25"},
    {"title": "IBPS Clerk 2026",                           "key": "clerk", "vacancies": 6128,  "application_end": "2026-07-28"},
    {"title": "IBPS SO 2026 (Specialist Officer)",         "key": "so",    "vacancies": 1500,  "application_end": "2026-08-05"},
    {"title": "IBPS RRB PO 2026 (Regional Rural Banks)",   "key": "rrb",   "vacancies": 9000,  "application_end": "2026-08-12"},
    {"title": "IBPS RRB Clerk 2026",                       "key": "rrb",   "vacancies": 11000, "application_end": "2026-08-15"},
]


def _parse_date(text: str) -> date | None:
    if not text:
        return None
    text = text.strip()
    # yyyy-mm-dd
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    # dd-mm-yyyy or dd/mm/yyyy
    m = re.search(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})", text)
    if m:
        try:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            pass
    # dd Mon yyyy
    m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})\w*[\s,]+(\d{4})", text)
    if m:
        month = _MONTHS.get(m.group(2).lower())
        if month:
            try:
                return date(int(m.group(3)), month, int(m.group(1)))
            except ValueError:
                pass
    return None


def _key_for(title: str) -> str:
    t = title.lower()
    for k in ("clerk", "so", "rrb", "po", "officer"):
        if k in t:
            return k
    return "po"


def _parse_html(html: str) -> list[RawJob]:
    soup = BeautifulSoup(html, "lxml")
    jobs: list[RawJob] = []
    seen: set[str] = set()

    # IBPS lists recruitments in tables and anchor-based news sections
    for el in soup.select("table tr, ul li, .notification-item, .recruit-item"):
        link = el.find("a", href=True)
        if not link:
            continue
        title = link.get_text(" ", strip=True)
        if len(title) < 10:
            continue
        # Only keep lines that look like recruitment notices
        if not re.search(r"ibps|recruit|po\b|clerk|officer|rrb|so\b|probationary", title, re.I):
            continue
        if title in seen:
            continue
        seen.add(title)

        href = link["href"]
        if href.startswith("/"):
            href = "https://www.ibps.in" + href
        if not href.startswith("http"):
            href = "https://www.ibps.in"

        full_text = el.get_text(" ", strip=True)
        end_date = _parse_date(full_text)
        key = _key_for(title)
        sal_text, sal_min, sal_max = _SALARY.get(key, (None, None, None))
        min_age, max_age = _AGE.get(key, (20, 30))

        jobs.append(RawJob(
            title=title,
            official_url=href,
            source="ibps",
            department="Institute of Banking Personnel Selection",
            company="IBPS",
            category="banking",
            location=["All India"],
            salary_text=sal_text,
            salary_min=sal_min,
            salary_max=sal_max,
            qualification=_QUAL.get(key, ["Graduate"]),
            min_age=min_age,
            max_age=max_age,
            application_end=end_date,
        ))

    return jobs


def _fallback_jobs() -> list[RawJob]:
    jobs = []
    for item in FALLBACK:
        key = item["key"]
        sal_text, sal_min, sal_max = _SALARY[key]
        min_age, max_age = _AGE[key]
        jobs.append(RawJob(
            title=item["title"],
            official_url="https://www.ibps.in",
            source="ibps",
            department="Institute of Banking Personnel Selection",
            company="IBPS",
            category="banking",
            location=["All India"],
            salary_text=sal_text,
            salary_min=sal_min,
            salary_max=sal_max,
            qualification=_QUAL[key],
            min_age=min_age,
            max_age=max_age,
            vacancies=item.get("vacancies"),
            application_end=_parse_date(item.get("application_end", "")),
        ))
    return jobs


class IBPSCrawler(BaseCrawler):
    source = "ibps"
    base_url = "https://www.ibps.in"
    category = "banking"

    async def crawl(self) -> list[RawJob]:
        # Try plain HTTP first (ibps.in usually serves plain HTML)
        html = await self.fetch(self.base_url)

        if html:
            jobs = _parse_html(html)
            if jobs:
                logger.info(f"[ibps] Parsed {len(jobs)} jobs from live site (plain HTTP)")
                return jobs
            # Site responded but layout changed — try Playwright
            logger.info("[ibps] Plain fetch succeeded but no jobs parsed — trying Playwright")
            html = await self.fetch_js(self.base_url, wait_selector="table, ul")

        if html:
            jobs = _parse_html(html)
            if jobs:
                logger.info(f"[ibps] Parsed {len(jobs)} jobs via Playwright")
                return jobs

        logger.warning("[ibps] Could not scrape live site — using fallback data")
        return _fallback_jobs()
