# 06 — Notification System

This is critical. Most job portals fail here. Strong notifications = high retention.

---

## Channels Overview

| Channel | Phase | Priority | Notes |
|---|---|---|---|
| Telegram public channel (auto-post) | Phase 1 | P0 | Biggest free growth channel |
| Telegram personal bot (matched alerts) | Phase 1 | P0 | Direct to user |
| Email daily digest | Phase 1 | P0 | Every morning 8 AM |
| WhatsApp Business API | Phase 2 | P1 | High open rate |
| Push notifications (mobile app) | Phase 2 | P1 | Requires app |

---

## Telegram Bot — Auto-Post New Jobs to Channel

```python
async def post_job_to_channel(job: Job):
    message = f"""
New Government Job Alert

{job.title}
{job.department}
Location: {', '.join(job.location[:3])}
Salary: {job.salary_text or 'As per norms'}
Qualification: {', '.join(job.qualification)}
Last Date: {job.application_end.strftime('%d %B %Y')}
Vacancies: {job.vacancies or 'Multiple'}

Apply Now: {job.official_url}
Full Details: https://yoursite.com/jobs/{job.job_id}

#GovernmentJobs #{job.category.replace(' ', '')} #Jobs2026
"""
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        parse_mode="Markdown"
    )
```

**Growth target:** 100,000 Telegram channel subscribers by Month 12.

---

## Alert Dispatcher — System Flow

```
New job inserted into DB
         |
         v
Alert Trigger fired (Celery task)
         |
         v
Query users matching: education + location + category preference
         |
         v
Filter by relevance score threshold (avoid noise)
         |
         v
Batch by notification channel
         |
     +---+---+---+---+
     |       |       |
  Email  Telegram  WhatsApp  Push
(daily  (instant) (Phase 2) (Phase 2)
digest)
```

---

## Email Daily Digest

**Send time:** Every morning at 8:00 AM

**Subject line:** `12 New Government Jobs Match Your Profile — 24 June 2026`

**Email body format:**
```
Good morning, [Name]!

Here are today's top matches for you:

1. SBI Clerk 2026 — All India — Rs.19,900/month
   Last Date: July 15   |   [Apply Now]

2. SSC CHSL 2026 — All India — Rs.18,000–25,000
   Last Date: July 20   |   [Apply Now]

3. Railway Group D — Multiple States — Rs.18,000/month
   Last Date: July 25   |   [Apply Now]

[View All 12 Matches]

---
[Manage Alert Preferences]   [Unsubscribe]
```

---

## WhatsApp Alert Format (Phase 2)

```
New Railway Vacancy
Posts: Group D
Last Date: 15 July 2026
Apply: [official link]

More jobs: [site link]
```

---

## Alert Fatigue Prevention

Without controls, users mute notifications within days.

- Minimum match score threshold before sending alert (e.g., score >= 60%)
- User-controlled frequency: Instant / Daily Digest / Weekly Summary
- Per-category mute option (e.g., "mute Defence jobs")
- "Quiet hours" setting (no alerts between 11 PM – 7 AM)
- Clear one-click unsubscribe in every email

---

## Personal Deadline Reminders

When a user saves a job:
- Auto-set reminder 3 days before application deadline
- Send via their preferred channel
- Format: "SBI Clerk deadline in 3 days — don't miss it! [Apply Now]"
