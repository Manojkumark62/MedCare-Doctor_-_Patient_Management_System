from pydantic import BaseModel
from typing import Optional


class MedicalRecordCreate(BaseModel):
    patient_id: int
    diagnosis: str
    treatment: str
    notes: Optional[str] = None


class MedicalRecordResponse(BaseModel):
    id: int
    patient_id: int
    diagnosis: str
    treatment: str

    class Config:
        from_attributes = True