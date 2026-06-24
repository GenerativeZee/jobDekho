from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from jose import jwt
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# In-memory OTP store for development — replace with Redis in production
_otp_store: dict[str, str] = {}


class SendOTPRequest(BaseModel):
    phone: str


class VerifyOTPRequest(BaseModel):
    phone: str
    otp: str


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(
        {"sub": user_id, "exp": expire},
        settings.SECRET_KEY,
        algorithm="HS256",
    )


@router.post("/send-otp")
async def send_otp(body: SendOTPRequest, db: AsyncSession = Depends(get_db)):
    otp = "123456" if settings.ENVIRONMENT == "development" else _generate_otp()
    _otp_store[body.phone] = otp

    if settings.ENVIRONMENT == "development":
        return {"message": "OTP sent", "dev_otp": otp}

    # TODO: integrate Fast2SMS here for production
    return {"message": "OTP sent"}


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(body: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    stored = _otp_store.get(body.phone)
    if not stored or stored != body.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    del _otp_store[body.phone]

    result = await db.execute(select(User).where(User.phone == body.phone))
    user = result.scalar_one_or_none()

    if not user:
        user = User(phone=body.phone, is_verified=True)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    user.last_login = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(str(user.id))
    return TokenResponse(access_token=token, user=UserResponse.model_validate(user))


def _generate_otp() -> str:
    import random
    return str(random.randint(100000, 999999))
