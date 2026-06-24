# 03 — Data Collection Architecture

This is the most critical and complex component. The platform lives or dies by data quality and freshness.

---

## Data Sources

### Source 1: Government Jobs

| Source | Website | Method |
|---|---|---|
| UPSC | upsc.gov.in | Crawler |
| SSC | ssc.nic.in | Crawler |
| Railway (RRB) | rrbcdg.gov.in + 20 regional boards | Crawler |
| IBPS | ibps.in | Crawler |
| SBI | sbi.co.in/careers | Crawler |
| RBI | rbi.org.in/careers | Crawler |
| NRA CET | nra.ac.in | Crawler |
| DRDO | drdo.gov.in | Crawler |
| ISRO | isro.gov.in | Crawler |
| State PSCs | 28 state websites | Crawler |
| Army / Navy / Air Force | joinindianarmy.nic.in etc. | Crawler |
| NHM / Health | nhm.gov.in | Crawler |
| High Courts / Judiciary | various state sites | Crawler |

**State PSC Priority (build in this order by population):**
UP → Bihar → MP → Rajasthan → Maharashtra → Gujarat → West Bengal → Odisha → Andhra Pradesh → Tamil Nadu

### Source 2: Private Jobs (Phase 2)

**Option A (Recommended Initially):** Scrape public careers pages of companies and startups.

**Option B (Later):** Partner with companies — they post directly. Becomes a revenue stream.

### Source 3: Internships (Phase 2)
- Startup internships
- Remote internships
- Paid internships
- Huge audience: students and freshers

---

## Crawler Architecture

```
Scheduler (cron every 6 hours)
       |
       v
Crawler Worker Pool (10 parallel workers)
       |
       v
Raw HTML → Parser (site-specific module per source)
       |
       v
Structured Data Extractor
       |
       v
Deduplication Layer (hash-based)
       |
       v
Validation Layer (deadline not past, link valid)
       |
       v
PostgreSQL Jobs Table
       |
       v
Search Index (Elasticsearch)
       |
       v
Alert Trigger (Celery task)
```

---

## Crawler Technical Stack
- **Scrapy** — static pages
- **Playwright** — JavaScript-rendered pages (SPAs)
- Modular per-site parser classes (one file per source)

```python
class SSCCrawler:
    base_url = "https://ssc.nic.in/portal/recruitment"
    schedule = "every 6 hours"
    parser = SSCParser()

    def extract(self, html) -> Job:
        # site-specific extraction logic
        pass
```

---

## Deduplication Strategy
- Hash on: `(title + department + deadline + location)`
- Store hash in Redis with TTL = deadline date
- If hash exists → skip (duplicate)
- If hash exists but salary/vacancies changed → update record

---

## Rate Limiting Rules
- Max 1 request per 2 seconds per domain
- Rotate user agents on every request
- Respect robots.txt
- Use residential proxy pool if IP gets blocked

---

## Error Handling
- Retry 3x with exponential backoff on failure
- Log all failures to monitoring (Sentry)
- Slack/email alert to admin if any source fails for 24+ hours
- Mark affected jobs as "unverified" until source recovers

---

## Special Data Challenges

| Challenge | Solution |
|---|---|
| Source site layout changes | Modular parsers + weekly automated regression tests + Slack alert on failure |
| Duplicate listings | Multi-field hash + fuzzy matching for near-duplicates |
| Jobs past deadline still showing | Nightly cleanup job removes expired listings |
| Missing salary info | Mark as "Not Disclosed"; don't block publish |
| Ambiguous location parsed | Human review queue for flagged cases |
| PDF-only notifications | PyMuPDF + pdfplumber for text extraction |
| Scanned PDF (image) | OCR pipeline: Tesseract / Google Vision API |
| Hindi / regional language content | Translation layer (optional in Phase 1) |

---

## Database Schema

### Jobs Table
```sql
CREATE TABLE jobs (
    job_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title             VARCHAR(300) NOT NULL,
    department        VARCHAR(200),
    company           VARCHAR(200),
    category          VARCHAR(100),       -- banking, railway, ssc, defence, psc
    sub_category      VARCHAR(100),
    location          TEXT[],             -- array of states/cities
    salary_min        INTEGER,
    salary_max        INTEGER,
    salary_text       VARCHAR(200),       -- raw text if salary is unstructured
    qualification     TEXT[],             -- 10th, 12th, graduate, postgraduate
    min_age           INTEGER,
    max_age           INTEGER,
    vacancies         INTEGER,
    notification_date DATE,
    application_start DATE,
    application_end   DATE,
    exam_date         DATE,
    official_url      TEXT NOT NULL,
    source            VARCHAR(100),       -- upsc, ssc, rrb, ibps, sbi, etc.
    raw_content       TEXT,
    content_hash      VARCHAR(64),        -- SHA256 for deduplication
    is_active         BOOLEAN DEFAULT TRUE,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    updated_at        TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_jobs_category      ON jobs(category);
CREATE INDEX idx_jobs_deadline      ON jobs(application_end);
CREATE INDEX idx_jobs_active        ON jobs(is_active);
CREATE INDEX idx_jobs_qualification ON jobs USING GIN(qualification);
CREATE INDEX idx_jobs_location      ON jobs USING GIN(location);
```

### Users Table
```sql
CREATE TABLE users (
    id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone            VARCHAR(15) UNIQUE,
    email            VARCHAR(255) UNIQUE,
    name             VARCHAR(200),
    age              INTEGER,
    gender           VARCHAR(20),
    city             VARCHAR(100),
    state            VARCHAR(100),
    education_level  VARCHAR(50),         -- 10th, 12th, diploma, graduate, pg, phd
    field_of_study   VARCHAR(100),
    skills           TEXT[],
    experience_years INTEGER DEFAULT 0,
    job_type_pref    VARCHAR(50)[],       -- government, private, internship
    location_pref    VARCHAR(100)[],      -- up to 5 preferred locations
    sector_pref      VARCHAR(100)[],      -- banking, railway, it, healthcare, etc.
    salary_min_exp   INTEGER,
    is_verified      BOOLEAN DEFAULT FALSE,
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    last_login       TIMESTAMPTZ
);
```

### Saved Jobs Table
```sql
CREATE TABLE saved_jobs (
    id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id  UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id   UUID REFERENCES jobs(job_id) ON DELETE CASCADE,
    saved_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, job_id)
);
```

### Job Views Table
```sql
CREATE TABLE job_views (
    id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id   UUID REFERENCES users(id),
    job_id    UUID REFERENCES jobs(job_id),
    viewed_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Alert Subscriptions Table
```sql
CREATE TABLE alert_subscriptions (
    id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id   UUID REFERENCES users(id),
    channel   VARCHAR(50),            -- email, telegram, whatsapp, push
    category  VARCHAR(100),           -- specific category or 'all'
    location  VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE
);
```

### Applications Tracking Table
```sql
CREATE TABLE applications (
    id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id   UUID REFERENCES users(id),
    job_id    UUID REFERENCES jobs(job_id),
    timestamp TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Elasticsearch Search Index Mapping

```json
{
  "mappings": {
    "properties": {
      "title":           { "type": "text", "analyzer": "english" },
      "department":      { "type": "keyword" },
      "category":        { "type": "keyword" },
      "location":        { "type": "keyword" },
      "qualification":   { "type": "keyword" },
      "salary_min":      { "type": "integer" },
      "salary_max":      { "type": "integer" },
      "application_end": { "type": "date" },
      "is_active":       { "type": "boolean" }
    }
  }
}
```

### Natural Language Search Flow
```
User types: "railway jobs in Bihar for 12th pass"
                      |
                      v
            NLP parsing layer
            - category: railway
            - location: Bihar
            - qualification: 12th
                      |
                      v
         Elasticsearch filtered query
                      |
                      v
  Ranked results (match score + recency + deadline proximity)
```
