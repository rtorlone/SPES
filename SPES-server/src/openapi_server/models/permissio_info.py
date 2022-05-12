# coding: utf-8

from __future__ import annotations

import re  # noqa: F401
from datetime import date, datetime  # noqa: F401
from typing import Any, Dict, List, Optional, Tuple  # noqa: F401
from uuid import UUID

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field  # noqa: F401


class PermissionPartialInfo(BaseModel):
    """
    PermissionPartialInfo - Modello che definisce le informazioni parziali di un permesso (in attesa di coferma o già dato) dell' utente specificato per il report indicato.

    """
    user_id: str
    created: date
    permission: bool
    report_id: str


class PermissionToModify(BaseModel):
    """
    PermissionPartialInfo - Modello che identifica un determinato permesso per il quale si vuole modificare lo stato.

    """
    user_id: str
    report_id: UUID
    permission: bool = Field(description="Questo è valore che verrò sostituito con quello già presente nel repository")


PermissionPartialInfo.update_forward_refs()
PermissionToModify.update_forward_refs()
