import os

from dotenv import load_dotenv
from jose import jwt
from passlib.context import CryptContext

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")

password_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return password_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_context.verify(
        password,
        hashed_password
    )


def create_access_token(user_id: int):
    payload = {
        "user_id": user_id
    }

    token = jwt.encode(
        payload,
        secret_key,
        algorithm=algorithm
    )

    return token