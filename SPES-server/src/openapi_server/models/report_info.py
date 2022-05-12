# coding: utf-8

from __future__ import annotations

import re  # noqa: F401
from datetime import date, datetime  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401
from uuid import UUID

from pydantic import AnyUrl, BaseModel, EmailStr, validator, Field  # noqa: F401


class ReportOnlyId(BaseModel):
    """
    ReportOnlyId - Modello che definisce l'id univoco del referto medico.

    """
    report_id: UUID


class ReportInfo(BaseModel):
    """
    ReportInfo - Modello che definisce le informazioni complete del referto medico.

    """
    report_id: UUID
    title: str
    upload_date: date
    permission: Optional[bool] = None
    pending: Optional[bool] = None


ReportInfo.update_forward_refs()
ReportOnlyId.update_forward_refs()
