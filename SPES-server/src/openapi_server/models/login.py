# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field  # noqa: F401


class Login(BaseModel):
    """NOTE:

    Login - Modello che definisce le credenziali di accesso dell'utente.

    """

    username: str
    password: str


class LoginResponse(BaseModel):
    """

    LoginResponse - Modello che definisce il body della response all'autenticazione.
    """

    jwt: Optional[str] = Field(None, description="Token di accesso associato all'utente. Tale token rispetta lo standard RFC 7519.")
    expires_at: Optional[datetime] = None
    first_access: Optional[bool] = Field(None, description="Indica qualora sia il primo accesso effettuato dall'utente. Utile per richiedere la modifica della pwd al primo accesso delle PF.")


Login.update_forward_refs()
LoginResponse.update_forward_refs()
