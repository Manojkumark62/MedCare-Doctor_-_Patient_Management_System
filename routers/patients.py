from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import database
from schemas.patients import PatientRegister, PatientResponse
from schemas.medical import MedicalRecordResponse
from models.users import User, UserRole
from dependencies.roles import role_required as RoleChecker
from services.patient_service import create_patient, get_patient_by_user_id, get_medical_history_for_user, get_all_medical_history

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/register", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def register_patient(
    payload: PatientRegister,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(RoleChecker([UserRole.ADMIN, UserRole.RECEPTIONIST]))
):
    return create_patient(payload, db, current_user)

@router.get("/profile", response_model=PatientResponse)
def view_patient_profile(
    user_id: int | None = None,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(RoleChecker([UserRole.PATIENT, UserRole.ADMIN, UserRole.RECEPTIONIST, UserRole.DOCTOR]))
):
    if str(current_user.role).lower() == UserRole.PATIENT.value:
        return get_patient_by_user_id(current_user.id, db)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="user_id query parameter is required for admin/receptionist/doctor access."
        )

    return get_patient_by_user_id(user_id, db)

@router.get("/medical-history", response_model=List[MedicalRecordResponse])
def view_medical_history(
    user_id: int | None = None,
    db: Session = Depends(database.get_db),
    current_user: User = Depends(RoleChecker([UserRole.PATIENT, UserRole.DOCTOR, UserRole.ADMIN]))
):
    if str(current_user.role).lower() == UserRole.PATIENT.value:
        return get_medical_history_for_user(current_user.id, db)

    if user_id is None:
        return get_all_medical_history(db)

    return get_medical_history_for_user(user_id, db)