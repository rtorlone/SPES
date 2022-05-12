import time
from typing import Dict

import jwt

JWT_SECRET = "SPESAPISECRET"

JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str, user_role: str, pf_id: str) -> Dict[str, str]:
    if pf_id == "":
        payload = {
            "user_id": user_id,
            "user_role": user_role,
            "expires": time.time() + 6000
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    else:
        payload = {
            "user_id": user_id,
            "user_role": user_role,
            "pf_id": pf_id,
            "expires": time.time() + 6000
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
