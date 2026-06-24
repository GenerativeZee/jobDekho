# 05 — AI Features

---

## Phase 1 — Basic Job Match Score (No LLM Required)

Rule-based scoring. Fast, cheap, and good enough for MVP.

```python
def calculate_match_score(user: User, job: Job) -> float:
    score = 0.0

    # Education match (40 points)
    if user.education_level in job.qualification:
        score += 40
    elif is_higher_education(user.education_level, job.qualification):
        score += 30  # overqualified but still eligible

    # Location match (25 points)
    if any(loc in job.location for loc in user.location_pref):
        score += 25
    elif 'All India' in job.location:
        score += 20

    # Category / sector match (25 points)
    if job.category in user.sector_pref:
        score += 25

    # Salary expectation match (10 points)
    if user.salary_min_exp and job.salary_min:
        if job.salary_min >= user.salary_min_exp:
            score += 10

    return round(score, 1)
```

**Displayed to user:**
```
You match 92% of requirements.
Apply Now.
```

---

## Phase 2 — LLM-Based Job Requirements Extraction

Use Claude API to parse unstructured job description text and PDFs into structured data.

```python
async def extract_job_requirements(raw_jd: str) -> dict:
    response = await claude.messages.create(
        model="claude-sonnet-4-6",
        messages=[{
            "role": "user",
            "content": f"""Extract structured data from this job notification:

{raw_jd}

Return JSON with:
- required_qualifications: list
- preferred_qualifications: list
- min_age: integer
- max_age: integer
- experience_required: string
- key_skills: list
- salary_structured: {{min, max, currency}}
"""
        }]
    )
    return json.loads(response.content[0].text)
```

---

## Phase 2 — AI Career Assistant

Users ask natural language questions. AI gives specific, actionable guidance.

```python
async def career_query(user_profile: dict, question: str) -> str:
    system_prompt = """You are a career counselor specializing in Indian
    government jobs, private sector placements, and freshers guidance.
    Give practical, specific advice based on the user's profile.
    Always mention specific exams, companies, or job roles by name."""

    user_context = f"""
    Education: {user_profile['education_level']} in {user_profile['field_of_study']}
    Experience: {user_profile['experience_years']} years
    Location: {user_profile['city']}, {user_profile['state']}
    Skills: {', '.join(user_profile['skills'])}
    """

    response = await claude.messages.create(
        model="claude-sonnet-4-6",
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"My profile:\n{user_context}\n\nQuestion: {question}"
        }]
    )
    return response.content[0].text
```

**Example interaction:**
```
User:  I am a B.Com graduate. What jobs can I apply for?

AI:    Based on your B.Com degree, here are your best options:

       Government Jobs:
       - IBPS PO / Clerk (Banking)
       - SBI PO / Clerk
       - SSC CGL (Tax Inspector, Auditor roles)
       - SSC CHSL
       - RBI Assistant

       Private Sector:
       - Accounts Executive at SMEs
       - Finance Analyst (entry level)
       - BPO / KPO roles

       Next step: Start with IBPS Clerk — exam is in November,
       high vacancy count, and B.Com gives you a syllabus advantage
       in Quantitative Aptitude and General Awareness.
```

---

## Phase 2 — Resume Analyzer

```
User uploads PDF resume
         |
         v
Extract text (PyMuPDF)
         |
         v
Send to Claude API with optional target job description
         |
         v
Output:
  - ATS compatibility score (0-100)
  - Missing keywords for target role
  - Missing resume sections
  - Specific line-by-line improvement suggestions
  - Skills gap vs current job market
  - Recommended certifications or courses
```

**Revenue:** Rs.99–499 per review. Available as:
- 1 free review/month on Premium plan
- Pay-per-use for free users

---

## Phase 3 — Exam Preparation Module (Premium Revenue)

For government exam aspirants — one of the highest-spend segments in India.

**Features:**
- Previous year questions (curated + auto-generated variations)
- Full-length mock tests with scoring and analysis
- AI-generated study plans based on exam date and current level
- Subject-specific AI tutor (ask questions, get explanations)
- Performance analytics (weak areas, improvement over time)

**Pricing:** Rs.199–999/month

**Why this is powerful:** Government exam aspirants currently spend Rs.5,000–50,000/year on coaching. A fraction of that at this price point is an easy sell, especially with AI personalization.
