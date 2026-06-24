# 08 — Challenges & Mitigations

---

## Legal & Compliance Challenges

| Challenge | Risk Level | Mitigation |
|---|---|---|
| Scraping government websites | Medium | Always link to official source; never re-host application forms; crawl respectfully with rate limits |
| Data accuracy liability | Medium | Show "Verify on official website before applying" disclaimer on every job detail page |
| User data privacy (DPDP Act 2023) | High | Privacy policy from Day 1; explicit consent at signup; right to delete data on request |
| Copyright of job notifications | Low | Government notifications are public domain in India |
| Fake or fraudulent job listings | Medium | Manual moderation queue; report button on every listing; verified source badge |
| Scraping private company pages | Medium | Only scrape public careers pages; don't store login-gated content |

**Key legal protection:** The platform does not host applications or collect user data on behalf of employers. It only aggregates and redirects. This is the same model as Google Jobs.

---

## Technical Challenges

| Challenge | Impact | Solution |
|---|---|---|
| Source website layout changes | Crawlers break silently, data stops | Modular per-site parsers; weekly automated regression tests; Slack/email alert if source fails |
| PDF-only job notifications | Data loss from major sources | PyMuPDF for text extraction; Tesseract / Google Vision OCR for scanned image PDFs |
| Government sites going down | Stale data, missed listings | Cache last known data; flag listing as "unverified" if source unreachable for 24+ hours |
| Deduplication at scale | Duplicate listings confuse users | SHA256 hash on (title + department + deadline + location); fuzzy matching for near-duplicates |
| Search relevance tuning | Users can't find what they need | Track click-through rate per result; A/B test ranking algorithms; user feedback loop |
| 28 different state PSC sites | Unsustainable maintenance | Prioritize top 10 states by population first; add remaining states progressively |
| Websites blocking crawlers | Data gaps | Rotating residential proxies; respectful crawl rate; randomize request intervals |
| JS-rendered pages (SPA sites) | Scrapy can't parse them | Use Playwright for JavaScript-heavy sources |
| Handling 20 RRB regional boards | High duplication, inconsistent formats | Consolidate into one Railway crawler with board-specific parsers |

---

## Growth & Distribution Challenges

| Challenge | Impact | Solution |
|---|---|---|
| Cold start — no users, no trust | No engagement loop to build on | Launch Telegram channel first; build audience before website; start posting manually day one |
| Low digital literacy in target users | High drop-off during onboarding | 3-step max onboarding; skip option always visible; Hindi UI option |
| Competing with Sarkari Result on SEO | Traffic loss for early months | Better UX + personalization + alerts — not just more jobs; target long-tail keywords they ignore |
| Alert fatigue | Users mute all notifications | Smart batching; relevance threshold; user-controlled frequency |
| Trust in data accuracy | Users don't rely on the portal | "Last verified: [timestamp]" on every listing; verified source badge; official link always prominent |
| Virality — users don't naturally share job portals | Slow organic growth | Referral program; sharable job cards optimized for WhatsApp forwarding |

---

## Operational Challenges

| Challenge | Solution |
|---|---|
| Crawler maintenance is permanent, ongoing work | Budget 20% of dev time permanently for crawler upkeep; treat crawlers as a product, not a project |
| Customer support for premium users | Set up helpdesk (Freshdesk / Crisp) before launching premium; create a FAQ and help center |
| Keeping job data fresh 24/7 | 6-hour crawl cycles + manual spot-checks for high-stakes exams (UPSC notification, RRB mega vacancy) |
| Moderating reported job listings | Build internal admin dashboard with flagged jobs review queue from Month 3 |
| Solo developer burnout risk | Modular architecture; document everything; prioritize ruthlessly; hire content ops early |

---

## Full Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Major crawler source permanently blocks IP | High | Medium | Residential proxy rotation; respectful crawl rate; try alternate data paths |
| Government portal redesign breaks all parsers | High | Medium | Weekly regression tests; Slack alerts on failure; budget time for emergency fixes |
| Low user retention after signup | Medium | High | Improve personalization; add push notifications; improve onboarding flow |
| Telegram channel growth stalls below 10K | Medium | High | Supplement with YouTube Shorts, WhatsApp community, SEO |
| Competitor with VC funding copies model | Medium | Low | Network effect and trust take time to build; execute faster |
| Regulatory action against scraping | Low | High | Always link official source; get legal consultation before launch |
| Server costs outpace revenue | Medium | Medium | Start very lean; scale infrastructure only when user numbers justify it |
| Key person dependency (solo dev) | High (if solo) | High | Document everything; build modular; no single points of failure in infra |
| User data breach | Low | Very High | Encrypt passwords; hash sensitive fields; HTTPS everywhere; regular security audits |
