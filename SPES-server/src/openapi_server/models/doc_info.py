# coding: utf-8

from __future__ import annotations

import re  # noqa: F401
from datetime import date, datetime  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401
from uuid import UUID
from typing import ForwardRef
from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field  # noqa: F401

DocInfo = ForwardRef('DocInfo')
DocPartialInfo = ForwardRef('DocPartialInfo')

class DocInfo(BaseModel):
    """
    DocInfo - Modello che definisce le informazioni complete di un documento amministrativo.

    """

    id: UUID
    tipologia: str
    upload_date: date
    entity: str
    number: Optional[str] = Field(default=None)
    place_of_issue: Optional[str] = Field(default=None)
    expiration_date: date = Field(
        description="La data non può essere antecedente al giorno corrente, inoltre non può essere antecedente a release_date")
    release_date: date = Field(
        description="La data non può essere antecedente al giorno corrente, inoltre non può essere precedente a release_date")

    @validator('release_date')
    def date_validator(cls, v, values):
        if v is not None:
            assert v <= date.today(), 'Data non valida(>= oggi)'
            if values.get("expiration_date"):
                assert v <= values["expiration_date"], 'la data di rilascio deve essere antecedente a quella di scadenza'
        return v


class DocPartialInfo(BaseModel):
    """
    DocInfo - Modello che definisce le informazioni parziali di un documento amministrativo.

    """

    id: UUID
    tipologia: str
    upload_date: date


DocInfo.update_forward_refs()
DocPartialInfo.update_forward_refs()
