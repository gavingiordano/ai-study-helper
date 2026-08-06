from app import auth
from app.database import get_session
from app.models import User, UserCreate, UserPublic
from fastapi import APIRouter, Depends, HTTPException
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