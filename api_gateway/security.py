from logging import getLogger, ERROR
from passlib.context import CryptContext

getLogger('passlib').setLevel(ERROR)

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str):
    return pwd_context.hash(password)


def is_password_legit(password: str, encrypted_password: str) -> bool:
    return pwd_context.verify(password, encrypted_password)


if __name__ == "__main__":
    pass
