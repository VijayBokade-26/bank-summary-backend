from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime
from enum import Enum

class ConsentUnit(str, Enum):
    MONTH = "MONTH"
    YEAR = "YEAR"
    DAY = "DAY"
    HOUR = "HOUR"
    INF = "INF"

class ConsentType(str, Enum):
    TRANSACTIONS = "TRANSACTIONS"
    PROFILE = "PROFILE"
    SUMMARY = "SUMMARY"

class ConsentDuration(BaseModel):
    unit: ConsentUnit
    value: int

class DataRange(BaseModel):
    from_date: datetime = Field(..., alias="from")
    to_date: datetime = Field(..., alias="to")

    class Config:
        populate_by_name = True

class ConsentRequest(BaseModel):
    vua: str
    consentDuration: ConsentDuration
    dataRange: DataRange
    consentTypes: List[ConsentType]

    @field_validator("vua")
    @classmethod
    def validate_vua(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid VUA format. Must contain '@'.")
        return v
