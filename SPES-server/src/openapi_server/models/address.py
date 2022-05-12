import re  # noqa: F401
from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional  # noqa: F401
from uuid import UUID

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field  # noqa: F401


class AddressTypeIdEnum(str, Enum):
    RESIDENZA = "FIX"
    DOMICILIO = "CUR"
    RESIDENZA_VIRTUALE_O_FITTIZIA = "VIR"


class Address(BaseModel):
    """
    Address - Modello che definisce l'indirizzo della PF.

    """
    from_date: date = Field(description="La data non può essere antecedente al giorno corrente")
    address: str
    geoarea_id: str
    address_type_id: AddressTypeIdEnum

    @validator('from_date', check_fields=False)
    def date_validator(cls, v):
        assert v <= date.today(), 'must be a valid Date'
        return v


class AddressWithId(Address):
    """
    AddressWithId - Modello che definisce l'id univoco del item dell'indirizzo.

    """
    id: UUID


Address.update_forward_refs()
AddressWithId.update_forward_refs()
