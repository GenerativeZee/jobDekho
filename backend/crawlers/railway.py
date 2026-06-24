"""
Railway Crawler — scrapes indianrailways.gov.in recruitment notices.

Railway recruitment is split across 20+ regional RRB boards.
We crawl the central Indian Railways recruitment page which aggregates
all active RRB notifications, then parse each notice.
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

# Salary by post level
_SALARY = {
    "group_d":  ("Rs.18,000 – Rs.56,900/month",  18000, 56900),
    "ntpc":     ("Rs.19,900 – Rs.35,400/month",  19900, 35400),
    "je":       ("Rs.35,400 – Rs.1,12,400/month",35400, 112400),
    "sse":      ("Rs.35,400 – Rs.1,12,400/month",35400, 112400),
    "aso":      ("Rs.29,200 – Rs.1,04,400/month",29200, 104400),
    "loco":     ("Rs.35,400 – Rs.1,12,400/month",35400, 112400),
    "constable":("Rs.21,700 – Rs.69,100/month",  21700, 69100),
    "default":  ("Rs.18,000 – Rs.56,900/month",  18000, 56900),
}

_QUAL = {
    "group_d":  ["10th", "ITI"],
    "ntpc":     ["12th", "Graduate"],
    "je":       ["Diploma", "Graduate"],
    "sse":      ["Graduate", "B.Tech"],
    "aso":      ["Graduate"],
    "loco":     ["10th", "ITI"],
    "constable":["12th"],
    "default":  ["10th"],
}

_AGE = {
    "group_d":  (18, 33),
    "ntpc":     (18, 33),
    "je":       (18, 33),
    "sse":      (18, 36),
    "aso":      (18, 30),
    "loco":     (18, 33),
    "constable":(18, 25),
    "default":  (18, 33),
}

_RRB_URL = "https://indianrailways.gov.in/railwayboard/view_section.jsp?lang=0&id=0,1,304,366,554"

FALLBACK: list[dict] = [
    {"title": "RRB Group D 2026 (Level 1 Posts)",              "key": "group_d",   "vacancies": 32438, "application_end": "2026-08-05", "url": _RRB_URL},
    {"title": "RRB NTPC Graduate Level 2026",                  "key": "ntpc",      "vacancies": 11558, "application_end": "2026-08-10", "url": _RRB_URL},
    {"title": "RRB NTPC 12th Level 2026",                      "key": "ntpc",      "vacancies": 3445,  "application_end": "2026-08-10", "url": _RRB_URL},
    {"title": "RRB JE 2026 (Junior Engineer)",                 "key": "je",        "vacancies": 7951,  "application_end": "2026-08-20", "url": _RRB_URL},
    {"title": "RRB SSE 2026 (Senior Section Engineer)",        "key": "sse",       "vacancies": 2022,  "application_end": "2026-08-20", "url": _RRB_URL},
    {"title": "RRB ALP 2026 (Assistant Loco Pilot)",           "key": "loco",      "vacancies": 18799, "application_end": "2026-09-01", "url": _RRB_URL},
    {"title": "RPF Constable 2026 (Railway Protection Force)", "key": "constable", "vacancies": 9000,  "application_end": "2026-09-10", "url": _RRB_URL},
]

# RRB regional pages to try in order
URLS = [
    "https://indianrailways.gov.in/railwayboard/view_section.jsp?lang=0&id=0,1,304,366,554",
    "https://www.rrbcdg.gov.in/",
    "https://www.rrbchennai.gov.in/",
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
    if "group d" in t or "level 1" in t:
        return "group_d"
    if "ntpc" in t:
        return "ntpc"
    if "sse" in t or "senior section" in t:
        return "sse"
    if "je" in t or "junior engineer" in t:
        return "je"
    if "alp" in t or "loco pilot" in t:
        return "loco"
    if "rpf" in t or "constable" in t or "protection" in t:
        return "constable"
    if "aso" in t or "office" in t:
        return "aso"
    return "default"


def _parse_html(html: str, base_url: str) -> list[RawJob]:
    soup = BeautifulSoup(html, "lxml")
    jobs: list[RawJob] = []
    seen: set[str] = set()

    for el in soup.select("table tr, ul li, .notice, .notification"):
        link = el.find("a", href=True)
        if not link:
            continue
        title = link.get_text(" ", strip=True)
        if len(title) < 15:
            continue
        # Real recruitment notices always include a year
        if not re.search(r"20\d\d", title):
            continue
        # Must mention specific railway job types — "railway" alone is too broad
        if not re.search(
            r"rrb|group.?d|ntpc|alp|loco.?pilot|rpf|je\b|sse|junior.?engineer|senior.?section|constable|vacancy|vacancies|\d+\s*post",
            title, re.I
        ):
            continue
        # Exclude non-job documents (reports, statistics, press releases)
        if re.search(r"statistic|annual.?report|press|statement|circular|policy|guideline|tender|corrigendum", title, re.I):
            continue
        if title in seen:
            continue
        seen.add(title)

        href = link["href"]
        if href.startswith("/"):
            domain = re.match(r"https?://[^/]+", base_url)
            href = (domain.group(0) if domain else "https://indianrailways.gov.in") + href
        if not href.startswith("http"):
            href = base_url

        full_text = el.get_text(" ", strip=True)
        end_date = _parse_date(full_text)
        key = _classify(title)

        sal_text, sal_min, sal_max = _SALARY[key]
        min_age, max_age = _AGE[key]

        jobs.append(RawJob(
            title=title,
            official_url=href,
            source="rrb",
            department="Railway Recruitment Boards",
            company="Indian Railways",
            category="railway",
            location=["All India"],
            salary_text=sal_text,
            salary_min=sal_min,
            salary_max=sal_max,
            qualification=_QUAL[key],
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
            official_url=item.get("url", _RRB_URL),
            source="rrb",
            department="Railway Recruitment Boards",
            company="Indian Railways",
            category="railway",
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


class RailwayCrawler(BaseCrawler):
    source = "rrb"
    base_url = URLS[0]
    category = "railway"

    async def crawl(self) -> list[RawJob]:
        # Try each Railway URL with plain HTTP first
        for url in URLS:
            html = await self.fetch(url)
            if html:
                jobs = _parse_html(html, url)
                if jobs:
                    logger.info(f"[rrb] Parsed {len(jobs)} jobs from {url}")
                    return jobs

        # Fallback to Playwright on the main page
        logger.info("[rrb] Plain HTTP yielded no results — trying Playwright")
        html = await self.fetch_js(self.base_url, wait_selector="table, ul, .notice")
        if html:
            jobs = _parse_html(html, self.base_url)
            if jobs:
                logger.info(f"[rrb] Parsed {len(jobs)} jobs via Playwright")
                return jobs

        logger.warning("[rrb] Could not scrape live site — using fallback data")
        return _fallback_jobs()
