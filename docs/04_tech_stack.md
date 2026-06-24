# 04 — Technology Stack & Architecture

---

## Stack Decisions

| Layer | Technology | Reason |
|---|---|---|
| Frontend | Next.js 14 (App Router) | SSR for SEO, fast, component-based |
| Styling | Tailwind CSS + Shadcn/ui | Fast development, consistent UI |
| Backend API | FastAPI (Python) | Async, fast, easy AI/ML integration |
| Database | PostgreSQL 16 | Reliable, JSONB support, mature |
| Cache | Redis 7 | Session storage, rate limiting, feed cache |
| Search | Elasticsearch 8 | Full-text search with filters |
| Crawlers | Scrapy + Playwright | Handles static and JS-rendered sites |
| Task Queue | Celery + Redis | Background jobs, scheduled crawls |
| Auth | JWT + OTP via Fast2SMS | Mobile-first, cheapest for India |
| File Storage | AWS S3 / Cloudflare R2 | Resumes, profile photos |
| Email | Resend / SendGrid | Transactional and digest emails |
| SMS | Fast2SMS | Cheapest OTP + alerts for India |
| Monitoring | Sentry + Uptime Robot | Error tracking, uptime alerts |

---

## System Architecture

```
User Browser / Mobile
         |
         v
    Cloudflare CDN
         |
         v
    Next.js (Frontend — SSR + Static)
         |
         v
    FastAPI (Backend API)
    |-- Auth Service
    |-- Jobs Service
    |-- User Service
    |-- Alert Service
    |-- AI Service
         |
         v
    +------------+----------+--------------+
    |            |          |              |
 PostgreSQL    Redis    Elasticsearch   S3/R2
 (primary DB) (cache)   (search)      (files)

    Background Workers (Celery)
    |-- Crawlers (every 6 hours, per source)
    |-- Alert dispatcher (on new job insert)
    |-- Deduplication worker
    |-- AI matching scorer
    |-- Nightly cleanup (remove expired jobs)
```

---

## API Endpoints

### Authentication
```
POST /api/auth/send-otp          Send OTP to mobile number
POST /api/auth/verify-otp        Verify OTP, return JWT
POST /api/auth/google            Google OAuth login
POST /api/auth/logout            Invalidate session
```

### Users
```
GET  /api/user/profile           Get current user profile
PUT  /api/user/profile           Update profile fields
GET  /api/user/saved-jobs        List saved jobs
POST /api/user/saved-jobs/{id}   Save a job
DEL  /api/user/saved-jobs/{id}   Remove saved job
```

### Jobs
```
GET  /api/jobs                   Paginated feed (personalized if authenticated)
GET  /api/jobs/{job_id}          Job detail page data
GET  /api/jobs/search?q=...      Full-text search with filters
GET  /api/jobs/categories        Category list with counts
```

### Alerts
```
POST /api/alerts/subscribe       Subscribe to alert channel + category
GET  /api/alerts/subscriptions   List active subscriptions
DEL  /api/alerts/{id}            Unsubscribe from alert
```

### Admin (Internal)
```
GET  /api/admin/jobs             Paginated job management
PUT  /api/admin/jobs/{id}        Edit or moderate a listing
DEL  /api/admin/jobs/{id}        Remove a listing
GET  /api/admin/crawlers/status  Health check for all crawlers
POST /api/admin/crawlers/run     Trigger a crawler manually
```

---

## Frontend Performance Requirements
- First Contentful Paint < 1.5 seconds
- Mobile-first layout (60%+ users are on mobile)
- Works on 2G / slow 3G — optimize images, use lazy loading
- Offline support for saved jobs (PWA, Phase 2)

---

## Hosting Plan

| Phase | Hosting | Estimated Monthly Cost |
|---|---|---|
| Phase 1 (MVP) | VPS — 4 vCPU, 8GB RAM | Rs.2,000–3,000 |
| Phase 2 | Upgraded VPS or managed cloud services | Rs.15,000–25,000 |
| Year 2+ | AWS / Azure / GCP (scales with revenue) | Variable |

---

## Tools for Development & Operations

| Purpose | Tool |
|---|---|
| Project management | Linear / Jira |
| Communication | Slack |
| Documentation | Notion |
| Error monitoring | Sentry |
| Product analytics | PostHog / Mixpanel |
| Uptime monitoring | Uptime Robot |
| Customer support | Freshdesk / Crisp |
| CI/CD | GitHub Actions |
