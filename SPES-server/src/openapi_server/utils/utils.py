import random
import string
import uuid
from typing import Set

import numpy as np
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_username(firstname: str, lastname: str) -> str:
    """
    Costruisce uno username a partire dal firstname e lastname
    :param firstname:
    :param lastname:
    :return: Lo username
    """

    if not firstname and not lastname:
        return "Anonymous" + str(np.random.randint(1000)) + str(np.random.randint(1000))

    if not firstname:
        return lastname + + str(np.random.randint(1000))

    return firstname[:3] + "." + lastname + str(np.random.randint(1000))


def generate_random_password() -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(8))
    return password


def verify_password(plain_password: str, hashed_password: str):
    print(get_password_hash(plain_password))
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_list_of_ids(n: int) -> Set[str]:
    result = set()
    while len(result) <= n:
        result.add(str(uuid.uuid4()))
    return result
