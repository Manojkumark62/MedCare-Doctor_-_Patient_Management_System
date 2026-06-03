from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from dependencies.roles import role_required
from schemas.medical import MedicalRecordCreate
from schemas.prescription import PrescriptionCreate
from services.medical_service import create_medical_record, get_patient_records
from services.prescription_service import create_prescription, get_prescriptions

router = APIRouter(prefix="/doctor", tags=["Doctor"])

@router.post("/medical-records")
def add_medical_record(data: MedicalRecordCreate, db: Session = Depends(get_db), current_user=Depends(role_required(["DOCTOR"]))):

    return create_medical_record(data, db, current_user)    

@router.get("/medical-records/{patient_id}")
def patient_records(patient_id: int, db: Session = Depends(get_db), current_user=Depends(role_required(["DOCTOR", "ADMIN"]))):

    return get_patient_records(patient_id, db)

@router.post("/prescriptions")
def add_prescription(data: PrescriptionCreate, db: Session = Depends(get_db), current_user=Depends(role_required(["DOCTOR"]))):

    return create_prescription(data, db, current_user)  

@router.get("/prescriptions/{patient_id}")
def patient_prescriptions(patient_id: int, db: Session = Depends(get_db), current_user=Depends(role_required(["DOCTOR", "PATIENT", "ADMIN"]))):

    return get_prescriptions(patient_id, db)