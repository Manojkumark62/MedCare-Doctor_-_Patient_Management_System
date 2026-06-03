from pydantic import BaseModel
from typing import List


class PrescriptionItemCreate(BaseModel):
    medicine_name: str
    dosage: str
    duration: str


class PrescriptionCreate(BaseModel):
    appointment_id: int
    patient_id: int
    doctor_id: int
    notes: str
    medicines: List[PrescriptionItemCreate]
