import re  # noqa: F401
from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional  # noqa: F401
from uuid import UUID

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field  # noqa: F401


class MaritalStatusEnum(str, Enum):
    CONVIVENTE = "COH"
    DIVORZIATO = "DIV"
    SEPARATO_LEGALMENTE = "LSE"
    CONIUGATO = "MAR"
    SINGLE = "SIN"
    VEDOVO = "WID"


class MaritalStatus(BaseModel):
    """
    MaritalStatus - Modello che definisce lo stato civile della PF.

    """
    marital_status_code: MaritalStatusEnum
    from_date: date = Field(description="La data non può essere antecedente al giorno corrente")

    @validator('from_date', check_fields=False)
    def date_validator(cls, v):
        assert v <= date.today(), 'must be a valid Date'
        return v


class MaritalStatusWithId(MaritalStatus):
    """
    MaritalStatusWithId - Modello che definisce l'id univoco del item dello stato civile.

    """
    id: UUID


MaritalStatus.update_forward_refs()
MaritalStatusWithId.update_forward_refs()
