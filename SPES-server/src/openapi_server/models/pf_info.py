# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from enum import Enum
from typing import Any, Dict, List, Optional  # noqa: F401
from uuid import uuid4, UUID

from pycountry import countries
from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field, constr  # noqa: F401

from models.address import Address
from models.citizenship import Citizenship
from models.marital_status import MaritalStatus


class GenderEnum(str, Enum):
    male = 'M'
    female = 'F'


class PfInfo(BaseModel):
    """
    PfInfo - Modello che definisce le informazioni complete di una PF.

    """

    cf: Optional[constr(max_length=16, min_length=16)] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    fullname: Optional[str] = None
    gender: Optional[GenderEnum] = None
    nicknames: Optional[str] = None
    birth_date: Optional[date] = Field(None, description="La data non può essere antecedente al giorno corrente")
    birth_nation_id: Optional[str] = Field("ITA", description="Questo campo adotta lo standard ISO 3166-1 Alpha3")
    birth_geoarea_id: Optional[str] = None
    birth_city: Optional[str] = None
    cui_code: Optional[str] = None
    sanitary_district_id: Optional[str] = None
    is_foreign: Optional[bool] = None
    is_anonymous: Optional[bool] = None
    verified: Optional[bool] = None
    is_dead: Optional[bool] = None
    death_date: Optional[date] = Field(None, description="La data non può essere antecedente al giorno corrente")
    marital_status_list: Optional[List[MaritalStatus]] = Field(None, description="Lista (opzionale) dello storico degli stati civili.")
    address_list: Optional[List[Address]] = Field(None, description="Lista (opzionale) dello storico degli indirizzi.")
    citizenship_list: Optional[List[Citizenship]] = Field(None, description="Lista (opzionale) dello storico delle cittadinanze.")

    @validator('birth_nation_id')
    def birth_nation_id_validator(cls, v):
        assert countries.get(alpha_3=v), 'must be ISO-3166 alpha3 compliant'
        return v

    @validator('birth_date', 'death_date', check_fields=False)
    def date_validator(cls, v):
        if v:
            assert v <= date.today(), 'must be a valid Date'
        return v

    @validator('is_anonymous', check_fields=False)
    def anonymous_validator(cls, v, values):
        if v:
            assert (not values["firstname"] and not values["lastname"]), 'must be anonymous'
        else:
            assert (values["firstname"] and values["lastname"]), 'must not be anonymous'
        return v


class PfInfoWithIds(PfInfo):
    """
    PfInfoWithIds - Modello che definisce le informazioni complete di una PF.

    Tale modello estende PFInfo introducendo l'id univoco della PF.
    Le liste presenti in PFInfo ora sono dizionari, le cui chiavi fanno riferimento alle istanze dei rispettivi item all'iterno del repository.

    """

    pf_id: UUID
    marital_status_list: Optional[Dict[str, MaritalStatus]] = Field(None, description="Dizionario (opzionale) dello storico degli stati civili.")
    address_list: Optional[Dict[str, Address]] = Field(None, description="Dizionario (opzionale) dello storico degli indirizzi.")
    citizenship_list: Optional[Dict[str, Citizenship]] = Field(None, description="Dizionario (opzionale) dello storico delle cittadinanze.")


class PfInfoWithIdsForUpdate(BaseModel):
    """
    PfInfoWithIdsForUpdate - Modello che definisce le informazioni necessarie per un aggiornamento della PF.

    """
    pf_id: UUID
    cf: Optional[constr(max_length=16, min_length=16)] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    fullname: Optional[str] = None
    gender: Optional[GenderEnum] = None
    nicknames: Optional[str] = None
    birth_date: Optional[date] = Field(None, description="La data non può essere antecedente al giorno corrente")
    birth_nation_id: Optional[str] = Field("ITA", description="Questo campo adotta lo standard ISO 3166-1 Alpha3")
    birth_geoarea_id: Optional[str] = None
    birth_city: Optional[str] = None
    cui_code: Optional[str] = None
    sanitary_district_id: Optional[str] = None
    is_foreign: Optional[bool] = None
    is_anonymous: Optional[bool] = None
    verified: Optional[bool] = None
    is_dead: Optional[bool] = None
    death_date: Optional[date] = Field(None, description="La data non può essere antecedente al giorno corrente")
    marital_status_list_to_add: Optional[List[MaritalStatus]] = Field(None, description="Lista (opzionale) dello storico degli stati civili da aggiungere")
    address_list_to_add: Optional[List[Address]] = Field(None, description="Lista (opzionale) dello storico degli indirizzi da aggiungere")
    citizenship_list_to_add: Optional[List[Citizenship]] = Field(None, description="Lista (opzionale) dello storico delle cittadinanze da aggiungere")
    marital_status_list_to_delete: Optional[List[str]] = Field(None, description="Lista (opzionale) dello storico degli stati civili da rimuovere. Sono specificati solamente gli id")
    address_list_to_delete: Optional[List[str]] = Field(None, description="Lista (opzionale) dello storico degli indirizzi da rimuovere. Sono specificati solamente gli id")
    citizenship_list_to_delete: Optional[List[str]] = Field(None, description="Lista (opzionale) dello storico delle cittadinanze da rimuovere. Sono specificati solamente gli id")
    marital_status_list_to_update: Optional[Dict[str, MaritalStatus]] = Field(None, description="Dizionario (opzionale) dello storico degli stati civili da aggiornare")
    address_list_to_update: Optional[Dict[str, Address]] = Field(None, description="Dizionario (opzionale) dello storico degli indirizzi da aggiornare")
    citizenship_list_to_update: Optional[Dict[str, Citizenship]] = Field(None, description="Dizionario (opzionale) dello storico delle cittadinanze da aggiornare")

    @validator('birth_nation_id')
    def birth_nation_id_validator(cls, v):
        assert countries.get(alpha_3=v), 'must be ISO-3166 alpha3 compliant'
        return v

    @validator('birth_date', 'death_date', check_fields=False)
    def date_validator(cls, v):
        if v:
            assert v <= date.today(), 'must be a valid Date'
        return v

    @validator('is_anonymous', check_fields=False)
    def anonymous_validator(cls, v, values):
        if v:
            assert (not values["firstname"] and not values["lastname"]), 'must be anonymous'
        else:
            assert (values["firstname"] and values["lastname"]), 'must not be anonymous'
        return v


class PFPartialInfoWithIds(BaseModel):
    """
    PFPartialInfoWithIds - Modello che definisce informazioni parziali della PF.
    """
    pf_id: UUID
    firstname: Optional[str]
    lastname: Optional[str]
    cf: Optional[constr(max_length=16, min_length=16)] = None
    cui_code: Optional[str]
    gender: Optional[GenderEnum]
    birth_date: Optional[date] = Field(None, description="La data non può essere antecedente al giorno corrente")
    nicknames: Optional[str]
    is_foreign: Optional[bool]
    is_anonymous: Optional[bool]
    is_dead: Optional[bool]
    verified: Optional[bool]

    @validator('birth_date', check_fields=False)
    def date_validator(cls, v):
        if v:
            assert v <= date.today(), 'must be a valid Date'
        return v

    @validator('is_anonymous', check_fields=False)
    def anonymous_validator(cls, v, values):
        if v:
            assert (not values["firstname"] and not values["lastname"]), 'must be anonymous'
        else:
            assert (values["firstname"] and values["lastname"]), 'must not be anonymous'
        return v


class PfId(BaseModel):
    """
    PfId - Modello che definisce l'id della PF.

    """

    id: UUID


class PfUserInfo(BaseModel):
    """
    PfUserInfo - Modello che definisce le credenziali di accesso della PF.

    """
    username: str
    password: str


PfInfoWithIds.update_forward_refs()
PfInfo.update_forward_refs()
PfUserInfo.update_forward_refs()
PFPartialInfoWithIds.update_forward_refs()
PfId.update_forward_refs()
