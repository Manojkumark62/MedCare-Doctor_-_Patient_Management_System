from typing import Any, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.users import User
from models.patients import Patient
from models.medical_records import MedicalRecord
from services.audit_service import create_audit_log
from services.notification_service import create_notification


def _normalize_payload(payload: Any) -> dict:
    if hasattr(payload, "model_dump"):
        return payload.model_dump()
    if isinstance(payload, dict):
        return payload
    if hasattr(payload, "dict"):
        return payload.dict(exclude_unset=True)
    return {k: getattr(payload, k) for k in getattr(payload, "__dict__", {})}


def create_patient(payload: Any, db: Session, current_user: Optional[User] = None) -> Patient:
    data = _normalize_payload(payload)

    parent_user = db.query(User).filter(User.id == data.get("user_id")).first()
    if not parent_user:
        raise HTTPException(
            status_code=404,
            detail="Registration failed: User account does not exist. Create the user via /auth/register first."
        )

    existing = db.query(Patient).filter(Patient.user_id == data.get("user_id")).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="A patient profile is already mapped to this user account."
        )

    patient = Patient(**data)
    db.add(patient)
    db.commit()
    db.refresh(patient)

    if current_user:
        create_audit_log(db, current_user.id, "CREATE", "PATIENT")
        create_notification(
            db,
            parent_user.id,
            "Patient Profile Created",
            "A patient profile has been created for your account."
        )

    return patient


def get_patient_by_user_id(user_id: int, db: Session) -> Patient:
    patient = db.query(Patient).filter(Patient.user_id == user_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient profile record could not be found.")
    return patient

def get_medical_history_for_user(user_id: int, db: Session):
    patient = db.query(Patient).filter(Patient.user_id == user_id).first()
    if not patient:
        return []
    return db.query(MedicalRecord).filter(MedicalRecord.patient_id == patient.id).all()

def get_all_medical_history(db: Session):
    return db.query(MedicalRecord).all()