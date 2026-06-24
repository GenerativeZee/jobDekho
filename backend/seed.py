"""Run with: python seed.py"""
import asyncio
import hashlib
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.models.job import Job

engine = create_async_engine(settings.DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

JOBS = [
    {
        "title": "SBI Clerk 2026",
        "department": "State Bank of India",
        "company": "State Bank of India",
        "category": "banking",
        "location": ["All India"],
        "salary_min": 17900,
        "salary_max": 47920,
        "salary_text": "Rs.17,900 - Rs.47,920/month",
        "qualification": ["graduate"],
        "min_age": 20,
        "max_age": 28,
        "vacancies": 13735,
        "application_start": date(2026, 6, 1),
        "application_end": date(2026, 7, 15),
        "official_url": "https://sbi.co.in/careers",
        "source": "sbi",
    },
    {
        "title": "SSC CHSL 2026",
        "department": "Staff Selection Commission",
        "company": "Government of India",
        "category": "ssc",
        "location": ["All India"],
        "salary_min": 19900,
        "salary_max": 63200,
        "salary_text": "Rs.19,900 - Rs.63,200/month",
        "qualification": ["12th"],
        "min_age": 18,
        "max_age": 27,
        "vacancies": 3712,
        "application_start": date(2026, 6, 10),
        "application_end": date(2026, 7, 20),
        "official_url": "https://ssc.nic.in",
        "source": "ssc",
    },
    {
        "title": "IBPS PO 2026",
        "department": "Institute of Banking Personnel Selection",
        "company": "IBPS",
        "category": "banking",
        "location": ["All India"],
        "salary_min": 36000,
        "salary_max": 63840,
        "salary_text": "Rs.36,000 - Rs.63,840/month",
        "qualification": ["graduate"],
        "min_age": 20,
        "max_age": 30,
        "vacancies": 4455,
        "application_start": date(2026, 6, 15),
        "application_end": date(2026, 7, 25),
        "official_url": "https://ibps.in",
        "source": "ibps",
    },
    {
        "title": "Railway Group D 2026",
        "department": "Railway Recruitment Boards",
        "company": "Indian Railways",
        "category": "railway",
        "location": ["All India"],
        "salary_min": 18000,
        "salary_max": 56900,
        "salary_text": "Rs.18,000 - Rs.56,900/month",
        "qualification": ["10th", "ITI"],
        "min_age": 18,
        "max_age": 33,
        "vacancies": 32438,
        "application_start": date(2026, 6, 20),
        "application_end": date(2026, 8, 5),
        "official_url": "https://indianrailways.gov.in",
        "source": "rrb",
    },
    {
        "title": "SSC CGL 2026",
        "department": "Staff Selection Commission",
        "company": "Government of India",
        "category": "ssc",
        "location": ["All India"],
        "salary_min": 25500,
        "salary_max": 81100,
        "salary_text": "Rs.25,500 - Rs.81,100/month",
        "qualification": ["graduate"],
        "min_age": 18,
        "max_age": 32,
        "vacancies": 17727,
        "application_start": date(2026, 6, 5),
        "application_end": date(2026, 7, 10),
        "official_url": "https://ssc.nic.in",
        "source": "ssc",
    },
    {
        "title": "UPSC Civil Services 2026",
        "department": "Union Public Service Commission",
        "company": "Government of India",
        "category": "upsc",
        "location": ["All India"],
        "salary_text": "Rs.56,100 - Rs.2,50,000/month (IAS/IPS/IFS)",
        "qualification": ["graduate"],
        "min_age": 21,
        "max_age": 32,
        "vacancies": 1056,
        "application_start": date(2026, 2, 5),
        "application_end": date(2026, 3, 4),
        "exam_date": date(2026, 5, 25),
        "official_url": "https://upsc.gov.in",
        "source": "upsc",
    },
    {
        "title": "RRB NTPC Graduate Level 2026",
        "department": "Railway Recruitment Boards",
        "company": "Indian Railways",
        "category": "railway",
        "location": ["All India"],
        "salary_min": 19900,
        "salary_max": 35400,
        "salary_text": "Rs.19,900 - Rs.35,400/month",
        "qualification": ["graduate"],
        "min_age": 18,
        "max_age": 33,
        "vacancies": 11558,
        "application_start": date(2026, 6, 25),
        "application_end": date(2026, 8, 10),
        "official_url": "https://indianrailways.gov.in",
        "source": "rrb",
    },
    {
        "title": "IBPS Clerk 2026",
        "department": "Institute of Banking Personnel Selection",
        "company": "IBPS",
        "category": "banking",
        "location": ["All India"],
        "salary_min": 13075,
        "salary_max": 35370,
        "salary_text": "Rs.13,075 - Rs.35,370/month",
        "qualification": ["graduate"],
        "min_age": 20,
        "max_age": 28,
        "vacancies": 6128,
        "application_start": date(2026, 7, 1),
        "application_end": date(2026, 7, 28),
        "official_url": "https://ibps.in",
        "source": "ibps",
    },
    {
        "title": "Delhi Police Constable 2026",
        "department": "Delhi Police",
        "company": "Ministry of Home Affairs",
        "category": "police",
        "location": ["Delhi"],
        "salary_min": 21700,
        "salary_max": 69100,
        "salary_text": "Rs.21,700 - Rs.69,100/month",
        "qualification": ["12th"],
        "min_age": 18,
        "max_age": 25,
        "vacancies": 5000,
        "application_start": date(2026, 7, 5),
        "application_end": date(2026, 8, 15),
        "official_url": "https://delhipolice.gov.in",
        "source": "delhi_police",
    },
    {
        "title": "NHM UP Community Health Officer 2026",
        "department": "National Health Mission UP",
        "company": "Government of UP",
        "category": "health",
        "location": ["Uttar Pradesh"],
        "salary_min": 25000,
        "salary_max": 25000,
        "salary_text": "Rs.25,000/month",
        "qualification": ["BSc Nursing", "GNM"],
        "min_age": 21,
        "max_age": 40,
        "vacancies": 5591,
        "application_start": date(2026, 6, 18),
        "application_end": date(2026, 7, 30),
        "official_url": "https://nhm.up.gov.in",
        "source": "nhm_up",
    },
]


def make_hash(job: dict) -> str:
    key = f"{job['title']}{job.get('department','')}{job.get('application_end','')}"
    return hashlib.sha256(key.encode()).hexdigest()


async def seed():
    async with AsyncSessionLocal() as db:
        for job_data in JOBS:
            job_data["content_hash"] = make_hash(job_data)
            job = Job(**job_data)
            db.add(job)

        try:
            await db.commit()
            print(f"Seeded {len(JOBS)} jobs successfully.")
        except Exception as e:
            await db.rollback()
            print(f"Error seeding (jobs may already exist): {e}")


if __name__ == "__main__":
    asyncio.run(seed())
