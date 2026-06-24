# 09 — Execution Plan

---

## Team Requirements

### Phase 1 (Solo or 2-person)

| Role | Responsibility | Notes |
|---|---|---|
| Full-stack Developer | Frontend + Backend + Crawlers + DevOps | Can be done solo |
| Content Curator | Verify job data, write descriptions, spot-check | Part-time or outsource on Fiverr |

### Phase 2 (3–5 person team)

| Role | Responsibility |
|---|---|
| Backend Developer | API development, crawlers, AI integration, infrastructure |
| Frontend Developer | Next.js UI, mobile experience, performance optimization |
| Growth / SEO | Telegram channel, YouTube Shorts, content strategy, SEO pages |
| Content Operations | Job data quality, manual verification, fraud detection |
| Customer Support | Premium user queries, refunds, helpdesk management |

---

## Month-by-Month Timeline

### Month 1 — Foundation
- [ ] Register domain (shortlist: sarkarikhoj.in / jobsarkari.com / bharatijobs.in)
- [ ] Set up GitHub repository and folder structure
- [ ] Deploy basic FastAPI backend + Next.js frontend on VPS
- [ ] Set up PostgreSQL + Redis
- [ ] Build first 3 crawlers: SSC, UPSC, IBPS
- [ ] Basic job listing page live (no login required to view)
- [ ] Launch Telegram channel — start posting jobs manually
- [ ] Register Fast2SMS account for OTP

### Month 2 — Core Features
- [ ] OTP-based auth + Google Login
- [ ] User profile creation (3-screen onboarding)
- [ ] Personalized job feed (basic match scoring)
- [ ] Job detail page with all fields
- [ ] Elasticsearch integration + basic search
- [ ] Filters: category, location, qualification, deadline
- [ ] 10+ crawlers live (add SBI, RBI, DRDO, ISRO, top 3 state PSCs)
- [ ] Email alert daily digest (using Resend / SendGrid)
- [ ] Telegram bot auto-posting new jobs to channel
- [ ] Saved jobs feature

### Month 3 — Polish & Beta Launch
- [ ] All major government sources crawled (25+ sources)
- [ ] SEO pages auto-generated (state, category, qualification, year)
- [ ] Deadline reminders (3 days before for saved jobs)
- [ ] Internal admin dashboard for job management
- [ ] Report job button on each listing
- [ ] Analytics setup (PostHog or Mixpanel)
- [ ] Beta launch to first 100 users
- [ ] Gather feedback, fix critical bugs

### Month 4–6 — Growth Phase
- [ ] AI match score displayed on job cards
- [ ] Mobile performance audit and fixes (target <1.5s FCP)
- [ ] SEO traffic starting to appear
- [ ] Telegram channel target: 10,000 subscribers
- [ ] Email list target: 5,000 subscribers
- [ ] Premium subscription plan launched (Rs.49–99/month)
- [ ] WhatsApp alert pilot (Phase 2 begins)
- [ ] Hindi UI option (at least job listing page)

### Month 7–12 — Expansion
- [ ] Resume analyzer feature
- [ ] AI career assistant (chat UI)
- [ ] Expand data: Freshers jobs + Private sector jobs
- [ ] Employer job posting portal (basic)
- [ ] Mock test module (Phase 3 early)
- [ ] React Native mobile app (iOS + Android)
- [ ] Referral program launch
- [ ] Target: 50,000 MAU, 1,000 premium subscribers, Rs.1L/month revenue

---

## Success Metrics (KPIs)

### Phase 1 Targets — By End of Month 3

| Metric | Target |
|---|---|
| Total jobs indexed | 10,000+ |
| Daily active users | 500+ |
| Telegram channel subscribers | 5,000+ |
| Email subscribers | 2,000+ |
| Profile completion rate | > 60% |
| Crawler uptime | > 95% |
| Mobile page load time | < 2 seconds |
| Job data freshness | < 6 hours |

### Phase 2 Targets — By End of Month 12

| Metric | Target |
|---|---|
| Monthly active users | 50,000+ |
| Telegram subscribers | 100,000+ |
| Email subscribers | 25,000+ |
| Premium subscribers | 1,000+ |
| Monthly revenue | Rs.1 Lakh+ |
| Organic search traffic | 30,000+ sessions/month |
| Crawler sources live | 40+ |

---

## Immediate Next Steps (This Week)

1. **Register domain** — shortlist 3 options, check availability, register
2. **Set up GitHub repo** — create project folder structure
3. **Provision VPS** — deploy FastAPI + Next.js skeleton
4. **Build SSC crawler** — extract and store 100 real jobs
5. **Create Telegram channel** — post jobs manually for the first 2 weeks to test messaging
6. **Ship job listing page** — no auth required to view; just show jobs in a clean list

---

## Year 2 — Full Ecosystem Vision

At scale, the platform is no longer a job board. It becomes complete employment infrastructure:

| Feature | Status |
|---|---|
| Job Discovery (Government + Private + Internship) | Live |
| Personalized AI Feed | Live |
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

At that point, the platform competes not with Sarkari Result, but with Naukri, Shine, and LinkedIn — but specifically built for the Indian mass market.
