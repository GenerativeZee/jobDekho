# India Job Portal — Complete Project Plan

> One platform to discover every job in India. Built for Tier 2 and Tier 3 cities.

---

## Table of Contents

1. [Vision & Overview](#1-vision--overview)
2. [Market Analysis](#2-market-analysis)
3. [Niche Focus Decision](#3-niche-focus-decision)
4. [Phase 1 MVP](#4-phase-1-mvp)
5. [Detailed User Flows](#5-detailed-user-flows)
6. [Data Collection Architecture](#6-data-collection-architecture)
7. [Database Design](#7-database-design)
8. [Technology Stack](#8-technology-stack)
9. [Search Architecture](#9-search-architecture)
10. [AI Features](#10-ai-features)
11. [Notification System](#11-notification-system)
12. [Revenue Model](#12-revenue-model)
13. [Growth Strategy](#13-growth-strategy)
14. [Budget Estimates](#14-budget-estimates)
15. [Challenges & Mitigations](#15-challenges--mitigations)
16. [Team Requirements](#16-team-requirements)
17. [Timeline (12 Months)](#17-timeline-12-months)
18. [Success Metrics](#18-success-metrics)
19. [Risk Register](#19-risk-register)
20. [Immediate Next Steps](#20-immediate-next-steps)
21. [Year 2 Vision](#21-year-2-vision)

---

## 1. Vision & Overview

### Product
A centralized, AI-powered job discovery platform for India.
- **Phase 1:** Government Jobs only
- **Phase 2:** Freshers + Private Jobs
- **Year 2:** Complete employment ecosystem

### Problem
Job seekers today must visit SSC, UPSC, Railways, Banking websites, State PSC sites, company career portals, and multiple job boards separately. The market is completely fragmented.

Jobs are currently scattered across:
- Government portals (UPSC, SSC, RRB, IBPS)
- State government recruitment websites
- PSU careers pages
- Private company career pages
- Startup hiring pages
- Job boards
- Walk-in hiring notifications
- Apprenticeship programs
- Contract and freelance listings

Most unemployed people — especially in Tier 2/3 cities — miss opportunities simply because they never see them.

### Solution
One platform where users:
- Create a profile once (education, skills, location, job type)
- Instantly get all relevant openings in a personalized feed
- Receive alerts via Telegram, WhatsApp, and Email
- Apply by redirecting to the official source (avoids legal issues)

### Vision
Become the **"Google for Jobs in India"** — especially for Tier 2 and Tier 3 cities.

### Target Users
- Tier 2 / Tier 3 city job seekers
- Students and freshers aged 18–28
- Government exam aspirants
- Unemployed or underemployed adults with limited digital literacy

---

## 2. Market Analysis

### Market Size
- India: 900M+ working-age population
- ~40M actively searching for jobs at any point
- Government exam aspirants: 20M+/year
- UPSC, SSC, Railway, Banking exams draw tens of millions of applicants

### Competitor Weaknesses

| Platform | Core Weakness |
|---|---|
| Naukri, LinkedIn | No government jobs; Tier 1 city focused |
| Sarkari Result | Poor UX; no personalization; extremely ad-heavy |
| Employment News | Static PDF; no alerts; no search |
| FreshersWorld | Outdated UI; poor trust signals |
| State portals | Siloed by state; no aggregation |

### Opportunity
No existing platform combines all of the following:
- Government + Private + Internships in one personalized feed
- AI-based matching by education, location, and skills
- WhatsApp/Telegram-first real-time alerts
- Mobile-first UX built for low-bandwidth users
- Vernacular language support

---

## 3. Niche Focus Decision

### Option A: Government Jobs Only
**Pros:** Clear audience; high intent; deadline urgency drives repeat visits; strong SEO; exam prep = premium revenue
**Cons:** Slower job volume growth; premium-dependent revenue

### Option B: Freshers Jobs Only
**Pros:** Larger immediate audience; easier private company partnerships
**Cons:** High competition (Naukri, Internshala); lower retention

### Decision: Start with Government Jobs
Build trust in the most underserved, high-intent segment first. Expand to freshers and private jobs in Phase 2.

**Core Hypothesis:** A focused portal with 10,000 high-quality listings and excellent alerts will outperform a portal with 1 million poorly categorized jobs.

---

## 4. Phase 1 MVP

### Goal
- 5,000–10,000 curated government job listings
- Working user profile + personalized feed
- Email + Telegram alerts
- Basic search and filters

### Feature Priorities

| Feature | Priority | Complexity |
|---|---|---|
| OTP + Google Auth | P0 | Low |
| Profile creation | P0 | Low |
| Job listing + search | P0 | Medium |
| Filters (location, category, qualification) | P0 | Medium |
| Job detail page | P0 | Low |
| Telegram alert bot | P0 | Low |
| Email daily digest | P0 | Low |
| Save jobs | P1 | Low |
| Basic AI match score | P1 | Medium |
| Mobile-responsive UI | P0 | Medium |

### Deliberately Excluded from Phase 1
- Resume builder
- Mock tests / exam prep
- Employer dashboard
- WhatsApp integration
- Mobile app (web-first)
- Payment and premium features

---

## 5. Detailed User Flows

### Step 1: Sign Up

```
User lands on site
     |
     v
Enter mobile number
     |
     v
OTP sent via SMS (Fast2SMS)
     |
     v
OTP verified → Account created
     |
     v
Option: continue with Google instead
```

**Edge cases:**
- Wrong OTP → retry limit of 3 attempts
- Expired OTP → resend with 60-second cooldown
- Number already registered → redirect to login
- Google OAuth failure → fallback to OTP

---

### Step 2: Profile Creation (3-screen onboarding)

**Screen 1 — Basic Info**
- Name, Age, Gender (optional), City, State

**Screen 2 — Education**
- Highest Qualification: 10th / 12th / Diploma / Graduate / Postgraduate / PhD
- Field of Study: Science / Commerce / Arts / Engineering / Medical / Law
- Percentage / CGPA (optional), Year of Passing

**Screen 3 — Preferences**
- Job Type: Government / Private / Both / Internship
- Preferred Locations (multi-select, up to 5)
- Work Mode: On-site / Remote / Hybrid
- Preferred Sectors: Banking / Railways / Defence / IT / Healthcare / etc.
- Monthly Salary Expectation

**Skip Option:** Users can skip → see generic feed → get nudged to complete profile for personalization.

---

### Step 3: Personalized Job Feed

**Sorting Logic:**
1. Match score (education + location + sector match)
2. Application deadline proximity
3. Recency of posting

**Feed Card Layout:**
```
+------------------------------------------+
| SBI Clerk 2026                           |
| State Bank of India                      |
| All India  |  Rs.19,900/month            |
| Graduate   |  Last Date: 15 Jul          |
|                          [Save]  [Apply] |
+------------------------------------------+
```

**Filters:**
- Category: Banking / Railways / SSC / Defence / PSC / Other
- Location: State-level → District-level
- Education required
- Salary range
- Application deadline
- Posted within: Today / This week / This month

---

### Step 4: Job Detail Page

```
[Job Title]
[Company / Department]
Posted: [date]  |  Last Date: [date]
Salary: Rs.X – Rs.Y / month
Vacancies: [number]
Location: [cities/states]

Eligibility:
  - Education requirement
  - Age limit (min/max)
  - Experience required

Important Dates:
  - Notification date
  - Application start
  - Application end
  - Exam date

[Apply on Official Website]   → external redirect

[Save Job]  [Set Reminder]  [Share]

Source: SSC / UPSC / RRB / etc.
Verified: Official notification linked
Last verified: [timestamp]
```

---

### Step 5: Apply
Redirect to official source. Platform never hosts application forms.

---

## 6. Data Collection Architecture

### Government Job Sources

| Source | Website | Method |
|---|---|---|
| UPSC | upsc.gov.in | Crawler |
| SSC | ssc.nic.in | Crawler |
| Railway (RRB) | 20 regional RRB boards | Crawler |
| IBPS | ibps.in | Crawler |
| SBI | sbi.co.in/careers | Crawler |
| RBI | rbi.org.in/careers | Crawler |
| NRA CET | nra.ac.in | Crawler |
| DRDO | drdo.gov.in | Crawler |
| ISRO | isro.gov.in | Crawler |
| State PSCs | 28 states (prioritized) | Crawler |
| Defence (Army/Navy/Air Force) | joinindianarmy.nic.in | Crawler |
| NHM / Health | nhm.gov.in | Crawler |
| High Courts / Judiciary | various | Crawler |

**State PSC priority order:** UP → Bihar → MP → Rajasthan → Maharashtra → Gujarat → WB → Odisha → Andhra Pradesh → Tamil Nadu

### Crawler Pipeline

```
Scheduler (cron, every 6 hours)
       |
       v
Crawler Worker Pool (10 parallel workers)
       |
       v
Raw HTML → Site-Specific Parser
       |
       v
Structured Data Extractor
       |
       v
Deduplication Layer
       |
       v
Validation Layer (deadline check, link check)
       |
       v
PostgreSQL (jobs table)
       |
       v
Elasticsearch (search index)
       |
       v
Alert Trigger (Celery task)
```

### Crawler Stack
- **Scrapy** for static HTML pages
- **Playwright** for JavaScript-rendered pages
- One parser class per source (modular, easy to maintain)

### Deduplication
- Hash: `SHA256(title + department + deadline + location)`
- Store in Redis with TTL = application deadline date
- Skip if hash exists; update record if salary or vacancies changed

### Rate Limiting
- Max 1 request per 2 seconds per domain
- Rotate user agents on every request
- Respect robots.txt
- Residential proxy pool as fallback if blocked

### Error Handling
- Retry 3x with exponential backoff
- Log all failures to Sentry
- Slack/email alert if any source fails for 24+ hours
- Mark affected jobs as "unverified" until source recovers

### Special Handling

| Challenge | Solution |
|---|---|
| Source site layout changes | Modular parsers + weekly regression tests |
| PDF-only notifications | PyMuPDF / pdfplumber for text extraction |
| Scanned image PDFs | Tesseract / Google Vision OCR |
| Duplicate listings | Hash-based dedup + fuzzy match |
| Past-deadline jobs | Nightly cleanup job |
| Missing salary | Mark "Not Disclosed"; don't block publish |
| Hindi/regional content | Translation layer (Phase 2) |

---

## 7. Database Design

### Jobs Table
```sql
CREATE TABLE jobs (
    job_id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title             VARCHAR(300) NOT NULL,
    department        VARCHAR(200),
    company           VARCHAR(200),
    category          VARCHAR(100),
    sub_category      VARCHAR(100),
    location          TEXT[],
    salary_min        INTEGER,
    salary_max        INTEGER,
    salary_text       VARCHAR(200),
    qualification     TEXT[],
    min_age           INTEGER,
    max_age           INTEGER,
    vacancies         INTEGER,
    notification_date DATE,
    application_start DATE,
    application_end   DATE,
    exam_date         DATE,
    official_url      TEXT NOT NULL,
    source            VARCHAR(100),
    raw_content       TEXT,
    content_hash      VARCHAR(64),
    is_active         BOOLEAN DEFAULT TRUE,
    created_at        TIMESTAMPTZ DEFAULT NOW(),
    updated_at        TIMESTAMPTZ DEFAULT NOW()
);
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
    education_level  VARCHAR(50),
    field_of_study   VARCHAR(100),
    skills           TEXT[],
    experience_years INTEGER DEFAULT 0,
    job_type_pref    VARCHAR(50)[],
    location_pref    VARCHAR(100)[],
    sector_pref      VARCHAR(100)[],
    salary_min_exp   INTEGER,
    is_verified      BOOLEAN DEFAULT FALSE,
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    last_login       TIMESTAMPTZ
);
```

### Supporting Tables
```sql
CREATE TABLE saved_jobs (
    id       UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id  UUID REFERENCES users(id) ON DELETE CASCADE,
    job_id   UUID REFERENCES jobs(job_id) ON DELETE CASCADE,
    saved_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, job_id)
);

CREATE TABLE applications (
    id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id   UUID REFERENCES users(id),
    job_id    UUID REFERENCES jobs(job_id),
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE alert_subscriptions (
    id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id   UUID REFERENCES users(id),
    channel   VARCHAR(50),
    category  VARCHAR(100),
    location  VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE
);
```

---

## 8. Technology Stack

| Layer | Technology | Reason |
|---|---|---|
| Frontend | Next.js 14 (App Router) | SSR for SEO, fast, component-based |
| Styling | Tailwind CSS + Shadcn/ui | Fast development, consistent UI |
| Backend API | FastAPI (Python) | Async, fast, easy AI/ML integration |
| Database | PostgreSQL 16 | Reliable, JSONB support, mature |
| Cache | Redis 7 | Sessions, rate limiting, feed cache |
| Search | Elasticsearch 8 | Full-text search with filters |
| Crawlers | Scrapy + Playwright | Static + JS-rendered pages |
| Task Queue | Celery + Redis | Background jobs, scheduled crawls |
| Auth | JWT + OTP via Fast2SMS | Mobile-first, cheapest for India |
| File Storage | AWS S3 / Cloudflare R2 | Resumes, profile photos |
| Email | Resend / SendGrid | Transactional + digest emails |
| SMS | Fast2SMS | Cheapest OTP + alerts for India |
| Monitoring | Sentry + Uptime Robot | Error tracking, uptime |

### System Architecture
```
User Browser / Mobile
         |
    Cloudflare CDN
         |
    Next.js (SSR + Static)
         |
    FastAPI (Backend)
    |-- Auth Service
    |-- Jobs Service
    |-- User Service
    |-- Alert Service
    |-- AI Service
         |
    +----+------+---------------+
    |           |               |
 PostgreSQL   Redis      Elasticsearch

    Background Workers (Celery)
    |-- Crawlers (every 6h)
    |-- Alert dispatcher
    |-- Deduplication
    |-- Nightly cleanup
    |-- AI matching scorer
```

### API Endpoints

```
Auth:
  POST /api/auth/send-otp
  POST /api/auth/verify-otp
  POST /api/auth/google
  POST /api/auth/logout

Users:
  GET  /api/user/profile
  PUT  /api/user/profile
  GET  /api/user/saved-jobs
  POST /api/user/saved-jobs/{id}
  DEL  /api/user/saved-jobs/{id}

Jobs:
  GET  /api/jobs               Personalized paginated feed
  GET  /api/jobs/{id}          Job detail
  GET  /api/jobs/search?q=...  Full-text search
  GET  /api/jobs/categories    Category counts

Alerts:
  POST /api/alerts/subscribe
  GET  /api/alerts/subscriptions
  DEL  /api/alerts/{id}

Admin:
  GET  /api/admin/jobs
  PUT  /api/admin/jobs/{id}
  GET  /api/admin/crawlers/status
```

---

## 9. Search Architecture

### Elasticsearch Index
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
User: "railway jobs in Bihar for 12th pass"
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
  Results ranked by: match score + recency + deadline
```

---

## 10. AI Features

### Phase 1 — Basic Match Score (Rule-Based, No LLM)

```python
def calculate_match_score(user, job) -> float:
    score = 0.0

    # Education match (40 points)
    if user.education_level in job.qualification:
        score += 40
    elif is_higher_education(user.education_level, job.qualification):
        score += 30  # overqualified but eligible

    # Location match (25 points)
    if any(loc in job.location for loc in user.location_pref):
        score += 25
    elif 'All India' in job.location:
        score += 20

    # Category match (25 points)
    if job.category in user.sector_pref:
        score += 25

    # Salary match (10 points)
    if user.salary_min_exp and job.salary_min:
        if job.salary_min >= user.salary_min_exp:
            score += 10

    return round(score, 1)
```

### Phase 2 — LLM Job Requirements Extraction (Claude API)

```python
async def extract_job_requirements(raw_jd: str) -> dict:
    response = await claude.messages.create(
        model="claude-sonnet-4-6",
        messages=[{
            "role": "user",
            "content": f"Extract structured data from this job notification:\n\n{raw_jd}\n\nReturn JSON with required_qualifications, min_age, max_age, key_skills, salary_structured."
        }]
    )
    return json.loads(response.content[0].text)
```

### Phase 2 — AI Career Assistant

```python
async def career_query(user_profile: dict, question: str) -> str:
    response = await claude.messages.create(
        model="claude-sonnet-4-6",
        system="You are a career counselor for Indian job seekers. Give specific, actionable advice. Always name specific exams, companies, or roles.",
        messages=[{
            "role": "user",
            "content": f"Profile: {user_profile}\n\nQuestion: {question}"
        }]
    )
    return response.content[0].text
```

### Phase 2 — Resume Analyzer
```
Upload PDF resume
       |
Extract text (PyMuPDF)
       |
Send to Claude API + target job description
       |
Output:
  - ATS compatibility score (0–100)
  - Missing keywords
  - Missing resume sections
  - Line-by-line improvement suggestions
  - Skills gap vs job market
```
**Pricing:** Rs.99–499 per review. 1 free/month on Premium plan.

### Phase 3 — Exam Preparation (Premium)
- Previous year questions and mock tests
- AI-generated study plans based on exam date
- AI tutor for subject questions
- Performance analytics

**Pricing:** Rs.199–999/month

---

## 11. Notification System

### Channels by Phase

| Channel | Phase | Priority |
|---|---|---|
| Telegram public channel | Phase 1 | P0 |
| Telegram personal bot | Phase 1 | P0 |
| Email daily digest | Phase 1 | P0 |
| WhatsApp Business API | Phase 2 | P1 |
| Push notifications | Phase 2 | P1 |

### Telegram Auto-Post

```python
async def post_job_to_channel(job):
    message = f"""
New Government Job Alert

{job.title}
{job.department}
Location: {', '.join(job.location[:3])}
Salary: {job.salary_text or 'As per norms'}
Qualification: {', '.join(job.qualification)}
Last Date: {job.application_end.strftime('%d %B %Y')}
Vacancies: {job.vacancies or 'Multiple'}

Apply: {job.official_url}
Details: https://yoursite.com/jobs/{job.job_id}

#GovernmentJobs #{job.category} #Jobs2026
"""
    await bot.send_message(CHANNEL_ID, message)
```

**Target:** 100,000 Telegram subscribers by Month 12.

### Alert Dispatcher Flow
```
New job inserted in DB
       |
Alert Celery task fires
       |
Find matching users (education + location + category)
       |
Filter by relevance score threshold
       |
+------+------+--------+
|      |      |        |
Email Telegram WhatsApp Push
```

### Email Digest Format (8 AM daily)
```
Subject: 12 New Government Jobs Match Your Profile — 24 June 2026

Good morning, [Name]!

1. SBI Clerk 2026 — All India — Rs.19,900/month
   Last Date: July 15  |  [Apply Now]

2. SSC CHSL 2026 — All India — Rs.18,000–25,000
   Last Date: July 20  |  [Apply Now]

[View All 12 Matches]

[Manage Alerts]  [Unsubscribe]
```

### Alert Fatigue Prevention
- Minimum match score (60%) before alerting
- User-controlled frequency: Instant / Daily / Weekly
- Per-category mute option
- Quiet hours setting (11 PM – 7 AM)
- One-click unsubscribe on all emails

---

## 12. Revenue Model

### Phased Approach

| Phase | Revenue Focus |
|---|---|
| Months 1–6 | No revenue — build users and trust |
| Months 6–12 | Premium subscription only |
| Year 2 | All 5 revenue streams |

### Stream 1: Premium Subscription (Rs.49–199/month)

| Feature | Free | Premium |
|---|---|---|
| Browse jobs | Yes | Yes |
| Save jobs | Up to 10 | Unlimited |
| Email digest | Weekly | Daily |
| Telegram alerts | Yes | Instant + Priority |
| AI match score | No | Yes |
| Deadline reminders | No | Yes |
| WhatsApp alerts | No | Yes |
| Resume analysis | No | 1/month free |

### Stream 2: Featured Job Listings
Rs.500–5,000 per featured listing. Shown at top of feed with "Featured" badge.

### Stream 3: Resume Services
- AI Resume Analysis: Rs.99
- Expert Human Review: Rs.299–499
- ATS Optimization: Rs.199

### Stream 4: Exam Preparation (Rs.199–999/month)
Mock tests, previous year papers, AI study plans, AI tutor.

### Stream 5: Recruitment SaaS for SMEs
Companies post jobs, track candidates, schedule interviews.
Pricing: Rs.999–4,999/month.

### Stream 6: Affiliate Commissions
Partner with Unacademy, Testbook, Adda247. CPA model on course purchases.

### Year 2 Revenue Targets

| Stream | Monthly Target |
|---|---|
| Premium subscriptions | Rs.5–15 Lakh |
| Featured listings | Rs.2–8 Lakh |
| Exam prep | Rs.3–10 Lakh |
| Resume services | Rs.1–3 Lakh |
| Recruitment SaaS | Rs.5–20 Lakh |
| Affiliates | Rs.1–5 Lakh |

---

## 13. Growth Strategy

### Channel 1: Telegram
- Create channel before website launch
- Auto-post every job with deadline + apply link
- Target: 100,000 subscribers by Month 12
- Cost: Rs.0

### Channel 2: WhatsApp Community
- Job alerts community
- Manual curation initially; automate via Business API in Phase 2

### Channel 3: YouTube Shorts
- Daily video: "Top 10 Government Jobs Today"
- Template or AI-generated
- Drives brand awareness and SEO backlinks

### Channel 4: SEO (Most Scalable Long-Term)
Auto-generate high-traffic landing pages:
```
/government-jobs/ssc-jobs-2026
/government-jobs/railway-jobs-2026
/government-jobs/banking-jobs-2026
/jobs-by-qualification/jobs-for-12th-pass-2026
/jobs-by-state/government-jobs-in-delhi
/jobs-by-state/government-jobs-in-up
/jobs-by-state/government-jobs-in-bihar
```
Each page compounds over time — free recurring traffic indefinitely.

### Channel 5: Referral Program (Phase 2)
Refer a friend → both get 1 month Premium free. Viral word-of-mouth in Tier 2/3 cities.

### Channel 6: Content Marketing
Blog posts: "How to prepare for SBI PO", "SSC CGL syllabus 2026", etc.
Rank on Google → build authority and trust.

---

## 14. Budget Estimates

### Phase 1 (Months 1–3)

| Item | Monthly Cost |
|---|---|
| VPS (4 vCPU, 8GB RAM) | Rs.2,000–3,000 |
| PostgreSQL managed | Rs.1,500–2,500 |
| Redis managed | Rs.800–1,200 |
| Elasticsearch | Rs.2,000–3,500 |
| Fast2SMS OTP | Rs.500–1,000 |
| Email (Resend free tier) | Rs.0 |
| Domain + SSL | Rs.1,000/year |
| Proxy pool | Rs.1,500–3,000 |
| Uptime Robot | Rs.0–500 |
| **Total** | **Rs.9,000–15,000/month** |

### Phase 2 (Months 4–12)

| Item | Monthly Cost |
|---|---|
| Infrastructure (upgraded) | Rs.15,000–25,000 |
| Claude API (AI features) | Rs.5,000–15,000 |
| WhatsApp Business API | Rs.3,000–8,000 |
| SMS alerts | Rs.3,000–8,000 |
| Cloudflare Pro CDN | Rs.1,500 |
| Part-time staff | Rs.20,000–50,000 |
| **Total** | **Rs.47,500–1,07,500/month** |

---

## 15. Challenges & Mitigations

### Legal & Compliance

| Challenge | Risk | Mitigation |
|---|---|---|
| Scraping government websites | Medium | Link to official source; never re-host forms; crawl respectfully |
| Data accuracy liability | Medium | Disclaimer: "Verify on official website before applying" |
| DPDP Act 2023 compliance | High | Privacy policy; explicit consent; right to delete |
| Fake job listings | Medium | Report button; moderation queue; verified source badge |

### Technical

| Challenge | Solution |
|---|---|
| Source website layout changes | Modular parsers + weekly regression tests + Slack alerts |
| PDF-only notifications | PyMuPDF + OCR pipeline |
| Government sites going down | Cache fallback; "unverified" flag |
| Deduplication at scale | SHA256 hash + fuzzy matching |
| Websites blocking crawlers | Rotating proxies; respectful crawl rate |

### Growth & Distribution

| Challenge | Solution |
|---|---|
| Cold start | Launch Telegram first; post manually before website is ready |
| Low digital literacy | 3-step onboarding; skip option; Hindi UI |
| Competing with Sarkari Result | Better UX + personalization + alerts; not just more jobs |
| Alert fatigue | Smart batching; frequency controls; relevance threshold |

### Operational

| Challenge | Solution |
|---|---|
| Crawler maintenance (permanent) | Budget 20% dev time; treat as a product |
| Premium customer support | Freshdesk / Crisp helpdesk before paid launch |
| Job data freshness | 6-hour crawl cycles + manual checks for major exams |
| Reporting and moderation | Admin dashboard with flagged jobs queue |

---

## 16. Team Requirements

### Phase 1 (Solo / 2-person)

| Role | Responsibility |
|---|---|
| Full-stack Developer | Frontend + Backend + Crawlers + DevOps |
| Content Curator (part-time) | Verify job data, spot-check listings |

### Phase 2 (3–5 person)

| Role | Responsibility |
|---|---|
| Backend Developer | API, crawlers, AI integration, infra |
| Frontend Developer | Next.js, mobile performance, UX |
| Growth / SEO | Telegram, YouTube Shorts, content, SEO |
| Content Operations | Data quality, fraud detection |
| Customer Support | Premium users, helpdesk |

---

## 17. Timeline (12 Months)

### Month 1 — Foundation
- [ ] Register domain
- [ ] GitHub repo + folder structure
- [ ] FastAPI + Next.js deployed on VPS
- [ ] PostgreSQL + Redis set up
- [ ] First 3 crawlers: SSC, UPSC, IBPS
- [ ] Job listing page live (no auth required)
- [ ] Telegram channel launched — post manually

### Month 2 — Core Features
- [ ] OTP auth + Google Login
- [ ] Profile creation (3-screen)
- [ ] Personalized feed (basic matching)
- [ ] Job detail page
- [ ] Elasticsearch + search + filters
- [ ] 10+ crawlers live
- [ ] Email daily digest
- [ ] Telegram bot auto-posting
- [ ] Save jobs feature

### Month 3 — Beta Launch
- [ ] 25+ crawler sources live
- [ ] SEO pages auto-generated
- [ ] Deadline reminders
- [ ] Admin dashboard
- [ ] Report job button
- [ ] Analytics (PostHog / Mixpanel)
- [ ] Beta: 100 users
- [ ] Gather and act on feedback

### Month 4–6 — Growth
- [ ] AI match score displayed
- [ ] Mobile performance optimized (<1.5s FCP)
- [ ] Telegram: 10,000 subscribers
- [ ] Email list: 5,000 subscribers
- [ ] Premium subscription launched
- [ ] WhatsApp alerts started
- [ ] Hindi UI option

### Month 7–12 — Expansion
- [ ] Resume analyzer
- [ ] AI career assistant
- [ ] Freshers + private jobs added
- [ ] Employer posting portal
- [ ] Mock test module
- [ ] React Native mobile app
- [ ] Referral program

---

## 18. Success Metrics

### Phase 1 (End of Month 3)

| Metric | Target |
|---|---|
| Jobs indexed | 10,000+ |
| Daily active users | 500+ |
| Telegram subscribers | 5,000+ |
| Email subscribers | 2,000+ |
| Profile completion rate | >60% |
| Crawler uptime | >95% |
| Mobile page load | <2 seconds |

### Phase 2 (End of Month 12)

| Metric | Target |
|---|---|
| Monthly active users | 50,000+ |
| Telegram subscribers | 100,000+ |
| Email subscribers | 25,000+ |
| Premium subscribers | 1,000+ |
| Monthly revenue | Rs.1 Lakh+ |
| Organic search traffic | 30,000+ sessions/month |
| Crawler sources | 40+ |

---

## 19. Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Source blocks crawler IP | High | Medium | Proxy rotation; respectful crawl rate |
| Government portal redesign | High | Medium | Weekly regression tests; budget emergency fix time |
| Low user retention | Medium | High | Better personalization; push notifications |
| Telegram growth stalls | Medium | High | YouTube Shorts; WhatsApp; SEO |
| VC-funded competitor enters | Medium | Low | Execute faster; build network effect |
| Regulatory action (scraping) | Low | High | Link official source; legal consultation |
| Server costs outpace revenue | Medium | Medium | Start lean; scale only when justified |
| User data breach | Low | Very High | Encrypt passwords; HTTPS; security audits |
| Solo dev burnout | High (if solo) | High | Document everything; modular architecture |

---

## 20. Immediate Next Steps (This Week)

1. Register domain — shortlist: `sarkarikhoj.in` / `jobsarkari.com` / `bharatijobs.in`
2. Set up GitHub repository and project structure
3. Deploy FastAPI + Next.js skeleton on VPS
4. Build SSC crawler — store first 100 real jobs
5. Launch Telegram channel — post jobs manually to validate messaging
6. Ship job listing page — no auth required, just clean job cards

---

## 21. Year 2 Vision — Full Employment Ecosystem

At scale, this is no longer a job board. It becomes complete employment infrastructure for India.

| Feature | Status |
|---|---|
| Job Discovery (Govt + Private + Internship) | Live |
| AI Personalized Feed | Live |
| Telegram / WhatsApp / Email Alerts | Live |
| Resume Builder | Live |
| AI Resume Analyzer | Live |
| AI Career Assistant | Live |
| AI Interview Coach | Live |
| Skill Gap Analysis | Live |
| Online Courses Marketplace | Live |
| Government Exam Mock Tests | Live |
| Employer Job Posting Dashboard | Live |
| Recruitment SaaS for SMEs | Live |

At this point the platform competes not with Sarkari Result, but with Naukri, Shine, and LinkedIn — built specifically for the Indian mass market.
