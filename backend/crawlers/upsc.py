"""
UPSC Crawler — scrapes upsc.gov.in for civil services and group A/B recruitment.

UPSC publishes a "What's New" section with active notifications.
The page is largely static HTML but slow; we try plain HTTP then Playwright.
"""
import logging
import re
from datetime import date

from bs4 import BeautifulSoup

from crawlers.base import BaseCrawler, RawJob

logger = logging.getLogger(__name__)

_MONTHS = {
    "jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
    "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12,
}

_SALARY = {
    "ias":    ("Rs.56,100 – Rs.2,50,000/month", 56100, 250000),
    "ips":    ("Rs.56,100 – Rs.2,50,000/month", 56100, 250000),
    "ifs":    ("Rs.56,100 – Rs.2,50,000/month", 56100, 250000),
    "cse":    ("Rs.56,100 – Rs.2,50,000/month", 56100, 250000),
    "capf":   ("Rs.56,100 – Rs.1,77,500/month", 56100, 177500),
    "ese":    ("Rs.56,100 – Rs.1,77,500/month", 56100, 177500),
    "cms":    ("Rs.67,700 – Rs.2,08,700/month", 67700, 208700),
    "nda":    ("Rs.56,100 – Rs.1,10,700/month", 56100, 110700),
    "cds":    ("Rs.56,100 – Rs.1,77,500/month", 56100, 177500),
    "default":("Rs.56,100 – Rs.2,50,000/month", 56100, 250000),
}

_QUAL = {
    "nda":    ["12th"],
    "cds":    ["Graduate"],
    "default":["Graduate"],
}

_AGE = {
    "nda":    (16, 19),
    "cds":    (20, 24),
    "capf":   (20, 25),
    "default":(21, 32),
}

FALLBACK: list[dict] = [
    {"title": "UPSC Civil Services Exam 2026 (IAS/IPS/IFS)",  "key": "cse",  "vacancies": 1056, "application_end": "2026-03-04", "exam_date": "2026-05-25", "url": "https://upsc.gov.in/examinations/civil-services-examination"},
    {"title": "UPSC CAPF 2026 (Central Armed Police Forces)",  "key": "capf", "vacancies": 506,  "application_end": "2026-07-15",                           "url": "https://upsc.gov.in/examinations/central-armed-police-forces-ac-examination"},
    {"title": "UPSC Engineering Services Exam 2026",           "key": "ese",  "vacancies": 167,  "application_end": "2026-07-08",                           "url": "https://upsc.gov.in/examinations/engineering-services-examination"},
    {"title": "UPSC NDA 2026 (National Defence Academy) II",   "key": "nda",  "vacancies": 404,  "application_end": "2026-08-05",                           "url": "https://upsc.gov.in/examinations/nda-and-na-examination"},
    {"title": "UPSC CDS 2026 (Combined Defence Services) II",  "key": "cds",  "vacancies": 459,  "application_end": "2026-08-12",                           "url": "https://upsc.gov.in/examinations/combined-defence-services-examination"},
    {"title": "UPSC Combined Medical Services 2026",           "key": "cms",  "vacancies": 827,  "application_end": "2026-06-10",                           "url": "https://upsc.gov.in/examinations/combined-medical-services-examination"},
    {"title": "UPSC IFS 2026 (Indian Forest Service)",         "key": "ifs",  "vacancies": 150,  "application_end": "2026-03-04",                           "url": "https://upsc.gov.in/examinations/indian-forest-service-examination"},
]

URLS = [
    "https://upsc.gov.in/",
    "https://upsc.gov.in/examinations/active-examinations",
]


def _parse_date(text: str) -> date | None:
    if not text:
        return None
    text = text.strip()
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    m = re.search(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})", text)
    if m:
        try:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            pass
    m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})\w*[\s,]+(\d{4})", text)
    if m:
        month = _MONTHS.get(m.group(2).lower())
        if month:
            try:
                return date(int(m.group(3)), month, int(m.group(1)))
            except ValueError:
                pass
    return None


def _classify(title: str) -> str:
    t = title.lower()
    if "nda" in t:
        return "nda"
    if "cds" in t or "combined defence" in t:
        return "cds"
    if "capf" in t or "police force" in t:
        return "capf"
    if "engineering service" in t or "ese" in t:
        return "ese"
    if "medical" in t or "cms" in t:
        return "cms"
    if "forest" in t or "ifs" in t:
        return "ifs"
    if "civil service" in t or "ias" in t or "ips" in t:
        return "cse"
    return "default"


def _parse_html(html: str) -> list[RawJob]:
    soup = BeautifulSoup(html, "lxml")
    jobs: list[RawJob] = []
    seen: set[str] = set()

    for el in soup.select("table tr, .whats-new li, .notice li, .notification li, .active-exam li"):
        link = el.find("a", href=True)
        if not link:
            continue
        title = link.get_text(" ", strip=True)
        if len(title) < 15:
            continue
        # Real UPSC exam notifications always reference a year
        if not re.search(r"20\d\d", title):
            continue
        if not re.search(
            r"upsc|civil service|ias|ips|nda|cds|capf|ese|cms|ifs|recruitment|exam|vacancy|vacancies",
            title, re.I
        ):
            continue
        # Exclude result/instruction notices — we want open recruitment only
        if re.search(r"result|merit.?list|cut.?off|admit.?card|answer.?key|score.?card|instruction|mark|reserve.?list|lateral", title, re.I):
            continue
        if title in seen:
            continue
        seen.add(title)

        href = link["href"]
        if href.startswith("/"):
            href = "https://upsc.gov.in" + href
        if not href.startswith("http"):
            href = "https://upsc.gov.in"

        full_text = el.get_text(" ", strip=True)
        end_date = _parse_date(full_text)
        key = _classify(title)
        sal_text, sal_min, sal_max = _SALARY.get(key, _SALARY["default"])
        min_age, max_age = _AGE.get(key, _AGE["default"])

        jobs.append(RawJob(
            title=title,
            official_url=href,
            source="upsc",
            department="Union Public Service Commission",
            company="Government of India",
            category="upsc",
            location=["All India"],
            salary_text=sal_text,
            salary_min=sal_min,
            salary_max=sal_max,
            qualification=_QUAL.get(key, _QUAL["default"]),
            min_age=min_age,
            max_age=max_age,
            application_end=end_date,
        ))

    return jobs


def _fallback_jobs() -> list[RawJob]:
    jobs = []
    for item in FALLBACK:
        key = item["key"]
        sal_text, sal_min, sal_max = _SALARY.get(key, _SALARY["default"])
        min_age, max_age = _AGE.get(key, _AGE["default"])
        jobs.append(RawJob(
            title=item["title"],
            official_url=item.get("url", "https://upsc.gov.in/examinations/active-exams"),
            source="upsc",
            department="Union Public Service Commission",
            company="Government of India",
            category="upsc",
            location=["All India"],
            salary_text=sal_text,
            salary_min=sal_min,
            salary_max=sal_max,
            qualification=_QUAL.get(key, _QUAL["default"]),
            min_age=min_age,
            max_age=max_age,
            vacancies=item.get("vacancies"),
            application_end=_parse_date(item.get("application_end", "")),
            exam_date=_parse_date(item.get("exam_date", "")),
        ))
    return jobs


class UPSCCrawler(BaseCrawler):
    source = "upsc"
    base_url = URLS[0]
    category = "upsc"

    async def crawl(self) -> list[RawJob]:
        for url in URLS:
            html = await self.fetch(url)
            if html:
                jobs = _parse_html(html)
                if jobs:
                    logger.info(f"[upsc] Parsed {len(jobs)} jobs from {url}")
                    return jobs

        logger.info("[upsc] Plain HTTP yielded no results — trying Playwright")
        html = await self.fetch_js(self.base_url, wait_selector="table, ul, .notice")
        if html:
            jobs = _parse_html(html)
            if jobs:
                logger.info(f"[upsc] Parsed {len(jobs)} jobs via Playwright")
                return jobs

        logger.warning("[upsc] Could not scrape live site — using fallback data")
        return _fallback_jobs()
