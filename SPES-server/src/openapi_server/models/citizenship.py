import re  # noqa: F401
from datetime import date
from typing import Any, Dict, List, Optional  # noqa: F401
from uuid import UUID

from pycountry import countries
from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field  # noqa: F401


class Citizenship(BaseModel):
    """
    Citizenship - Modello che definisce la cittadinza della PF.

    """
    nation_id: str = Field(description="Questo campo adotta lo standard ISO 3166-1 Alpha3")
    from_date: date = Field(description="La data non può essere antecedente al giorno corrente")

    @validator('nation_id')
    def birth_nation_id_validator(cls, v):
        assert countries.get(alpha_3=v), 'must be ISO-3166 alpha3 compliant'
        return v

    @validator('from_date', check_fields=False)
    def date_validator(cls, v):
        assert v <= date.today(), 'must be a valid Date'
        return v


class CitizenshipWithId(Citizenship):
    """
    CitizenshipWithId - Modello che definisce l'id univoco del item della cittadinanza.

    """
    id: UUID


Citizenship.update_forward_refs()
CitizenshipWithId.update_forward_refs()
