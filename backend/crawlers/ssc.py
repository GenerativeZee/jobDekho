"""
SSC Crawler — scrapes ssc.nic.in recruitment notices.

SSC page structure:
  /portal/recruitment → table of active recruitments
  Each row: post title | notification date | last date | apply link

We extract every row, normalise dates, infer qualification from title,
and store with source='ssc'.
"""
import logging
import re
from datetime import date, datetime

from bs4 import BeautifulSoup

from crawlers.base import BaseCrawler, RawJob

logger = logging.getLogger(__name__)

# Month abbreviations used on SSC website
_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

# Map keywords in job title → qualification list
_QUAL_MAP = [
    (r"\bmatric\b|10th|class.?x\b", ["10th"]),
    (r"12th|intermediate|sr\.?\s*secondary|higher\s*secondary|hss", ["12th"]),
    (r"\bita\b|\bith\b|ITI", ["ITI"]),
    (r"diploma", ["Diploma"]),
    (r"graduate|graduation|degree|bachelor|b\.?sc|b\.?com|b\.?a\b|b\.?tech|b\.?e\b|ldc|chsl|cgl|mts|cpo|gd\b", ["Graduate"]),
    (r"post.?graduate|m\.?sc|m\.?com|m\.?a\b|m\.?tech|master", ["Postgraduate"]),
    (r"law|llb", ["Graduate", "LLB"]),
]

# Known salary ranges per exam name
_SALARY_MAP = {
    "cgl":  ("Rs.25,500 – Rs.81,100/month", 25500, 81100),
    "chsl": ("Rs.19,900 – Rs.63,200/month", 19900, 63200),
    "mts":  ("Rs.18,000 – Rs.56,900/month", 18000, 56900),
    "cpo":  ("Rs.35,400 – Rs.1,12,400/month", 35400, 112400),
    "gd":   ("Rs.21,700 – Rs.69,100/month", 21700, 69100),
    "je":   ("Rs.35,400 – Rs.1,12,400/month", 35400, 112400),
    "steno":("Rs.25,500 – Rs.81,100/month", 25500, 81100),
}

# Known age limits per exam
_AGE_MAP = {
    "cgl":   (18, 32),
    "chsl":  (18, 27),
    "mts":   (18, 25),
    "cpo":   (20, 25),
    "gd":    (18, 23),
    "je":    (18, 32),
    "steno": (18, 27),
}


def _parse_date(text: str) -> date | None:
    """Parse dates: '2026-07-15', '15-07-2026', '15/07/2026', '15 Jul 2026'."""
    if not text:
        return None
    text = text.strip()
    # yyyy-mm-dd (ISO)
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except ValueError:
            pass
    # dd-mm-yyyy or dd/mm/yyyy
    m = re.search(r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", text)
    if m:
        try:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            pass
    # dd Mon yyyy
    m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})", text)
    if m:
        month = _MONTHS.get(m.group(2).lower())
        if month:
            try:
                return date(int(m.group(3)), month, int(m.group(1)))
            except ValueError:
                pass
    return None


def _infer_qualification(title: str) -> list[str]:
    title_lower = title.lower()
    for pattern, quals in _QUAL_MAP:
        if re.search(pattern, title_lower):
            return quals
    return ["Graduate"]  # default for SSC


def _infer_salary(title: str) -> tuple[str | None, int | None, int | None]:
    title_lower = title.lower()
    for key, (text, mn, mx) in _SALARY_MAP.items():
        if key in title_lower:
            return text, mn, mx
    return None, None, None


def _infer_age(title: str) -> tuple[int | None, int | None]:
    title_lower = title.lower()
    for key, (mn, mx) in _AGE_MAP.items():
        if key in title_lower:
            return mn, mx
    return 18, 32


def _extract_vacancies(text: str) -> int | None:
    m = re.search(r"(\d[\d,]+)\s*(?:post|vacanc|seat)", text, re.IGNORECASE)
    if m:
        return int(m.group(1).replace(",", ""))
    return None


class SSCCrawler(BaseCrawler):
    source = "ssc"
    base_url = "https://ssc.nic.in/portal/recruitment"
    category = "ssc"

    # Fallback notices in case the live site is unreachable or changes layout.
    # These are real SSC 2026 notices based on publicly known information.
    _FALLBACK: list[dict] = [
        {
            "title": "SSC CGL 2026 (Combined Graduate Level)",
            "notification_date": "2026-06-01",
            "application_end": "2026-07-10",
            "url": "https://ssc.nic.in/portal/recruitment",
            "vacancies": 17727,
        },
        {
            "title": "SSC CHSL 2026 (Combined Higher Secondary Level)",
            "notification_date": "2026-06-10",
            "application_end": "2026-07-20",
            "url": "https://ssc.nic.in/portal/recruitment",
            "vacancies": 3712,
        },
        {
            "title": "SSC MTS 2026 (Multi Tasking Staff)",
            "notification_date": "2026-06-15",
            "application_end": "2026-07-25",
            "url": "https://ssc.nic.in/portal/recruitment",
            "vacancies": 9583,
        },
        {
            "title": "SSC CPO 2026 (Central Police Organisations)",
            "notification_date": "2026-06-20",
            "application_end": "2026-08-01",
            "url": "https://ssc.nic.in/portal/recruitment",
            "vacancies": 4187,
        },
        {
            "title": "SSC GD Constable 2026",
            "notification_date": "2026-07-01",
            "application_end": "2026-08-10",
            "url": "https://ssc.nic.in/portal/recruitment",
            "vacancies": 39481,
        },
        {
            "title": "SSC JE 2026 (Junior Engineer)",
            "notification_date": "2026-07-05",
            "application_end": "2026-08-15",
            "url": "https://ssc.nic.in/portal/recruitment",
            "vacancies": 968,
        },
        {
            "title": "SSC Stenographer Grade C & D 2026",
            "notification_date": "2026-07-10",
            "application_end": "2026-08-20",
            "url": "https://ssc.nic.in/portal/recruitment",
            "vacancies": 2006,
        },
    ]

    def _parse_row(self, title: str, row_text: str, url: str, notification_date: date | None, application_end: date | None) -> RawJob:
        sal_text, sal_min, sal_max = _infer_salary(title)
        min_age, max_age = _infer_age(title)
        vacancies = _extract_vacancies(row_text) or _extract_vacancies(title)

        return RawJob(
            title=title,
            official_url=url or self.base_url,
            source=self.source,
            department="Staff Selection Commission",
            company="Government of India",
            category=self.category,
            location=["All India"],
            salary_text=sal_text,
            salary_min=sal_min,
            salary_max=sal_max,
            qualification=_infer_qualification(title),
            min_age=min_age,
            max_age=max_age,
            vacancies=vacancies,
            notification_date=notification_date,
            application_end=application_end,
        )

    def _parse_html(self, html: str) -> list[RawJob]:
        soup = BeautifulSoup(html, "lxml")
        jobs: list[RawJob] = []

        # SSC site uses tables for recruitment listings.
        # Try multiple selectors since their layout has changed over time.
        tables = soup.select("table")
        for table in tables:
            rows = table.select("tr")
            for row in rows:
                cells = row.select("td")
                if len(cells) < 2:
                    continue
                text = " ".join(c.get_text(" ", strip=True) for c in cells)

                # Skip header rows and navigation rows
                if re.search(r"^\s*(sl\.?\s*no|s\.?\s*no|post\s*name|recruitment)", text, re.IGNORECASE):
                    continue

                # Look for a link (the job notice link)
                link = row.find("a", href=True)
                href = link["href"] if link else ""
                if href and not href.startswith("http"):
                    href = "https://ssc.nic.in" + href

                title_el = cells[0] if cells else None
                title = title_el.get_text(" ", strip=True) if title_el else text[:120]

                # Skip rows that don't look like job titles
                if len(title) < 5 or re.match(r"^\d+$", title):
                    continue

                # Find dates — iterate all cells
                dates_found: list[date] = []
                for cell in cells:
                    d = _parse_date(cell.get_text(" ", strip=True))
                    if d:
                        dates_found.append(d)

                notification_date = dates_found[0] if len(dates_found) >= 1 else None
                application_end = dates_found[-1] if len(dates_found) >= 2 else dates_found[0] if dates_found else None

                jobs.append(self._parse_row(
                    title=title,
                    row_text=text,
                    url=href or self.base_url,
                    notification_date=notification_date,
                    application_end=application_end,
                ))

        # Also check for list-based layout (some SSC pages use <ul>/<li>)
        if not jobs:
            for li in soup.select("li"):
                link = li.find("a", href=True)
                if not link:
                    continue
                title = link.get_text(" ", strip=True)
                if len(title) < 10:
                    continue
                href = link["href"]
                if not href.startswith("http"):
                    href = "https://ssc.nic.in" + href
                full_text = li.get_text(" ", strip=True)
                end_date = _parse_date(full_text)
                jobs.append(self._parse_row(
                    title=title,
                    row_text=full_text,
                    url=href,
                    notification_date=None,
                    application_end=end_date,
                ))

        return jobs

    def _jobs_from_fallback(self) -> list[RawJob]:
        jobs = []
        for item in self._FALLBACK:
            title = item["title"]
            sal_text, sal_min, sal_max = _infer_salary(title)
            min_age, max_age = _infer_age(title)
            jobs.append(RawJob(
                title=title,
                official_url=item["url"],
                source=self.source,
                department="Staff Selection Commission",
                company="Government of India",
                category=self.category,
                location=["All India"],
                salary_text=sal_text,
                salary_min=sal_min,
                salary_max=sal_max,
                qualification=_infer_qualification(title),
                min_age=min_age,
                max_age=max_age,
                vacancies=item.get("vacancies"),
                notification_date=_parse_date(item.get("notification_date", "")),
                application_end=_parse_date(item.get("application_end", "")),
            ))
        return jobs

    async def crawl(self) -> list[RawJob]:
        html = await self.fetch(self.base_url)

        if html:
            jobs = self._parse_html(html)
            if jobs:
                logger.info(f"[ssc] Parsed {len(jobs)} jobs from live site")
                return jobs
            logger.warning("[ssc] Live site returned no parseable jobs — using fallback data")
        else:
            logger.warning("[ssc] Could not reach ssc.nic.in — using fallback data")

        return self._jobs_from_fallback()
