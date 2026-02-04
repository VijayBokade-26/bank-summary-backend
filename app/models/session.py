from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class SessionDataRange(BaseModel):
    from_date: datetime = Field(..., alias="from")
    to_date: datetime = Field(..., alias="to")
    
    class Config:
        populate_by_name = True

class SessionRequest(BaseModel):
    dataRange: SessionDataRange
    consentId: str
    format: str = Field(default="json")
    
    @field_validator("consentId")
    @classmethod
    def validate_consent_id(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("consentId cannot be empty")
        # Basic UUID format validation (optional but recommended)
        if len(v.strip()) < 10:
            raise ValueError("consentId must be a valid identifier")
        return v.strip()
    
    @field_validator("format")
    @classmethod
    def validate_format(cls, v: str) -> str:
        allowed_formats = ["json", "xml"]
        if v.lower() not in allowed_formats:
            raise ValueError(f"format must be one of {allowed_formats}")
        return v.lower()
