import secrets

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def create_hashed_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_session_id() -> str:
    return secrets.token_urlsafe(32)