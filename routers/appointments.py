from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from dependencies.auth import get_current_user
from dependencies.roles import role_required
from schemas.appointments import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from services.appointment_service import book_appointment, get_all_appointments, get_appointment_by_id, reschedule_appointment, cancel_appointment

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentResponse, status_code=201)
def create_appointment(data: AppointmentCreate, db: Session = Depends(get_db), current_user=Depends(role_required(
            ["ADMIN", "PATIENT", "RECEPTIONIST"]))):
    return book_appointment(data, db, current_user)

@router.get("/", response_model=list[AppointmentResponse])
def appointments(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_all_appointments(db, current_user)

@router.get("/{appointment_id}", response_model=AppointmentResponse)
def appointment_by_id(appointment_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_appointment_by_id(appointment_id, db, current_user)

@router.put("/{appointment_id}", response_model=AppointmentResponse)
def reschedule(appointment_id: int, data: AppointmentUpdate, db: Session = Depends(get_db), current_user=Depends(role_required(
            ["ADMIN","RECEPTIONIST"]))):
    return reschedule_appointment(appointment_id, data, db, current_user)

@router.delete("/{appointment_id}")
def cancel(appointment_id: int, db: Session = Depends(get_db), current_user=Depends(role_required(
            ["ADMIN", "PATIENT", "RECEPTIONIST"]))):
    return cancel_appointment(appointment_id, db, current_user)

