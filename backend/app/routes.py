from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from backend.app.auth import pwd_context
from backend.app.database import get_session
from backend.app.models import User, UserCreate, UserPublic

router = APIRouter()


# Authentication routes

@router.post("/auth/signup", response_model=UserPublic)
async def signup(
    user_create: UserCreate,
    session: Session = Depends(get_session) # noqa: B008
) -> UserPublic:
    standard_email = user_create.email.strip().lower()
    existing_user = session.exec(select(User).where(User.email == standard_email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        name=user_create.name,
        email=standard_email,
        hashed_password=pwd_context.hash(user_create.password)
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user