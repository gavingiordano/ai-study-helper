from datetime import datetime, timedelta, timezone

from app import auth
from app.database import get_session
from app.models import User, UserCreate, UserLogin, UserPublic, UserSession
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

router = APIRouter()


# Authentication routes

@router.post("/auth/signup", response_model=UserPublic)
async def signup(
    user_create: UserCreate,
    session: Session = Depends(get_session) # noqa: B008
) -> UserPublic:
    normalized_email = user_create.email.strip().lower()
    existing_user = session.exec(select(User).where(User.email == normalized_email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        name=user_create.name,
        email=normalized_email,
        hashed_password=auth.create_hashed_password(user_create.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/auth/login", response_model=UserPublic)
async def login(
    user_login: UserLogin,
    response: Response,
    session: Session = Depends(get_session) # noqa: B008
) -> UserPublic:
    normalized_email = user_login.email.strip().lower()
    user = session.exec(select(User).where(User.email == normalized_email)).first()
    if not user or not auth.verify_password(user_login.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    session_id = auth.create_session_id()
    user_session = UserSession(
        session_id=session_id,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(hours=5),
    )
    session.add(user_session)
    session.commit()
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=5 * 3600,
    )
    return user