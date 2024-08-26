import bcrypt

fake_password = "gjf3ou3oGPJepJ"


def hash_password(password: str = fake_password) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(14)).decode("UTF-8")


def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


if __name__ == "__main__":
    pass
