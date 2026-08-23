from datetime import datetime, timezone

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    name: str | None = None
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)


class UserCreate(SQLModel):
    name: str | None = None
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserPublic(SQLModel):
    id: int
    name: str | None = None
    email: EmailStr


class UserLogin(SQLModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserSession(SQLModel, table=True):
    __tablename__ = "user_sessions"
    id: int | None = Field(default=None, primary_key=True)
    session_id: str = Field(index=True, unique=True)
    user_id: int = Field(foreign_key="users.id")
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)


class Course(SQLModel, table=True):
    __tablename__ = "courses"
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    name: str
    code: str | None  = None
    description: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)


class Document(SQLModel, table=True):
    __tablename__ = "documents"
    id: int | None = Field(default=None, primary_key=True)
    course_id: int = Field(foreign_key="courses.id")
    displayed_name: str
    original_filename: str
    file_path: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)