from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.medical_records import MedicalRecord
from models.patients import Patient
from services.audit_service import create_audit_log

def create_medical_record(data, db: Session, current_user):
    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    record = MedicalRecord(patient_id=data.patient_id, diagnosis=data.diagnosis, treatment=data.treatment, notes=data.notes, created_by=current_user.id)

    db.add(record)
    db.commit()
    db.refresh(record)

    create_audit_log(
        db,
        current_user.id,
        "CREATE",
        "MEDICAL_RECORD"
    )
    return record

def get_patient_records(patient_id, db):

    return db.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id).all()
