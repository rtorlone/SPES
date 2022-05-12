# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401
from uuid import uuid4, UUID

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field  # noqa: F401


class UserInfoForUpdate(BaseModel):
    """
    UserInfoForUpdate - Modello che definisce la vecchia password dell'utente e quella nuova che si desidera.

    """

    old_pwd: str = Field(description="La password antecedente.")
    new_pwd: str = Field(description="Il valore assegnato deve essere diverso da old_pwd.")

    @validator("new_pwd")
    def new_pwd_validator(cls, v, values):
        assert v != values["old_pwd"], "La nuova password deve essere diversa da quella precedente!"
        return v


class UserInfoWithPwd(BaseModel):
    """
    UserInfoWithPwd - Modello che definisce lo username.

    """
    username: str


UserInfoWithPwd.update_forward_refs()
UserInfoForUpdate.update_forward_refs()
