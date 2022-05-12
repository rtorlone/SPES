# coding: utf-8
from typing import Optional, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TokenModel(BaseModel):
    """Defines a token model."""
    user_id: str
    role: str
    expires: str
    pf_id: Optional[str]


"""
Qui di seguito sono definite le risposte generiche agli errori.
"""


class GenericNotFoundErrorResponse(BaseModel):
    entity_name: Optional[str] = None
    entity_id: Optional[str] = None


class GenericUnsupportedMediaTypeResponse(BaseModel):
    supported_media_type: List[str]


class GenericErrorResponse(BaseModel):
    description: Optional[str] = None
    args: Optional[str] = None
