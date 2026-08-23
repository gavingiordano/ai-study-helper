import secrets
from datetime import datetime, timezone

from app.database import get_session
from app.models import User, UserSession
from fastapi import Cookie, Depends, HTTPException
from pwdlib import PasswordHash
from sqlmodel import Session, select

password_hash = PasswordHash.recommended()


def create_hashed_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_session_id() -> str:
    return secrets.token_urlsafe(32)


def get_current_user(
    session_id: str | None = Cookie(default=None),
    session: Session = Depends(get_session) # noqa: B008
) -> User:
    if not session_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_session = session.exec(select(UserSession).where(UserSession.session_id == session_id)).first()
    if not user_session or user_session.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Session expired or invalid")
    user = session.exec(select(User).where(User.id == user_session.user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user