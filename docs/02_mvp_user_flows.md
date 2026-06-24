# 02 — Phase 1 MVP & User Flows

## Goal
Launch a functional portal with:
- 5,000–10,000 curated government job listings
- Working profile + personalized feed
- Email + Telegram alerts
- Basic search and filter

---

## High-Level User Flow

```
Sign Up (OTP / Google)
       ↓
Profile Creation (Education, Skills, Location, Job Type)
       ↓
Personalized Job Feed
       ↓
Job Detail Page (Source, Deadline, Salary, Eligibility)
       ↓
Apply → Redirect to Official Source
       ↓
Save Job / Set Alert
```

---

## Phase 1 Feature Priorities

| Feature | Priority | Complexity |
|---|---|---|
| OTP + Google Auth | P0 | Low |
| Profile creation | P0 | Low |
| Job listing + search | P0 | Medium |
| Filters (location, category, qualification) | P0 | Medium |
| Job detail page | P0 | Low |
| Telegram alert bot | P0 | Low |
| Email alerts | P0 | Low |
| Save jobs | P1 | Low |
| Basic AI matching score | P1 | Medium |
| Mobile-responsive UI | P0 | Medium |

## Deliberately Excluded from Phase 1
- Resume builder
- Mock tests
- Employer dashboard
- WhatsApp integration
- Mobile app (web-first)
- Payment / premium features

---

## Detailed User Flows

### Step 1: Sign Up

```
User lands on site
     ↓
Enter mobile number
     ↓
OTP sent via SMS (Fast2SMS / MSG91 / Twilio)
     ↓
OTP verified → Account created
     ↓
Option to continue with Google instead
```

**Edge Cases to Handle:**
- Wrong OTP → retry with limit (3 attempts)
- Expired OTP → resend option (60 second cooldown)
- Number already registered → redirect to login
- Google OAuth failure → fallback to OTP

---

### Step 2: Profile Creation (3-screen onboarding)

Breaking into 3 screens reduces drop-off.

**Screen 1: Basic Info**
- Name
- Age
- Gender (optional)
- City / State

**Screen 2: Education**
- Highest Qualification: 10th / 12th / Diploma / Graduate / Postgraduate / PhD
- Field of Study: Science / Commerce / Arts / Engineering / Medical / Law
- Percentage / CGPA (optional)
- Year of Passing

**Screen 3: Preferences**
- Job Type: Government / Private / Both / Internship
- Preferred Locations (multi-select, up to 5)
- Work Mode: On-site / Remote / Hybrid
- Preferred Sectors (Banking / Railways / Defence / IT / Healthcare, etc.)
- Monthly Salary Expectation

**Skip Option:** Allow skipping profile → show generic feed → nudge to complete profile for personalization.

---

### Step 3: Personalized Job Feed

**Sorting Logic:**
1. Match score (education + location + sector preference)
2. Application deadline proximity
3. Recency of posting

**Feed Card Design:**
```
┌─────────────────────────────────────┐
│  SBI Clerk 2026                     │
│  State Bank of India                │
│  All India  |  Rs.19,900/month      │
│  Graduate   |  Last Date: 15 Jul    │
│                       [Save] [Apply] │
└─────────────────────────────────────┘
```

**Filters Panel:**
- Category (Banking / Railways / SSC / Defence / PSC / Other)
- Location (State-level, then district)
- Education required
- Salary range
- Application deadline
- Posted within (Today / This week / This month)

---

### Step 4: Job Detail Page

```
Job Title
Company / Department
Posted: [date]  |  Last Date: [date]
Salary: Rs.X – Rs.Y per month
Vacancies: [number]
Location: [cities/states]

Eligibility:
- Education
- Age limit
- Experience

Important Dates:
- Notification: [date]
- Application Start: [date]
- Application End: [date]
- Exam Date: [date]

[Apply on Official Website] → external link

[Save Job]  [Set Reminder]  [Share]

Source: [SSC / Railway / UPSC etc.]
Verified: Official notification linked
Last checked: [timestamp]
```

---

### Step 5: Apply
Portal redirects to official source. This avoids legal issues around hosting application forms.

---

## Site Structure (Key Pages)

| Page | Purpose |
|---|---|
| `/` | Landing page + hero search |
| `/jobs` | Main job feed with filters |
| `/jobs/[id]` | Job detail |
| `/search` | Search results |
| `/category/banking` | Category-specific listing (SEO) |
| `/category/railway` | Category-specific listing (SEO) |
| `/location/delhi` | Location-specific listing (SEO) |
| `/profile` | User profile management |
| `/saved` | Saved jobs |
| `/alerts` | Alert management |
| `/auth/login` | Login / Signup |

---

## SEO Auto-Generated Pages

Each page targets a high-volume keyword:

```
/government-jobs/ssc-jobs-2026
/government-jobs/railway-jobs-2026
/government-jobs/banking-jobs-2026
/government-jobs/defence-jobs-2026
/jobs-by-qualification/jobs-for-12th-pass-2026
/jobs-by-qualification/jobs-for-graduates-2026
/jobs-by-state/government-jobs-in-delhi
/jobs-by-state/government-jobs-in-up
/jobs-by-state/government-jobs-in-bihar
/jobs-by-state/government-jobs-in-maharashtra
/jobs-by-state/government-jobs-in-rajasthan
```

Government job seekers are Google-heavy. These pages drive free recurring traffic.
