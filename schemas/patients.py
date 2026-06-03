from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PatientRegister(BaseModel):
    user_id: int
    full_name: str
    gender: str
    blood_group: Optional[str] = None
    emergency_contact: Optional[str] = None


class PatientResponse(BaseModel):
    id: int
    user_id: int
    full_name: str
    gender: str
    blood_group: Optional[str] = None
    emergency_contact: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
