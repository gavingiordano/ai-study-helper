from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def create_hashed_password(password: str) -> str:
    return password_hash.hash(password)