from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.appointments import Appointment
from models.patients import Patient
from models.doctors import Doctor
from services.notification_service import create_notification
from services.audit_service import create_audit_log

def book_appointment(data, db: Session, current_user):
    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    doctor = db.query(Doctor).filter(Doctor.id == data.doctor_id).first()
    if not doctor:
        # support using a doctor's user_id when doctor profile id is not available
        doctor = db.query(Doctor).filter(Doctor.user_id == data.doctor_id).first()

    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    existing = db.query(Appointment).filter(Appointment.doctor_id == doctor.id, Appointment.appointment_date == data.appointment_date).first()
    if existing:
        raise HTTPException(status_code=400, detail="Doctor already booked")

    appointment = Appointment(
        patient_id=data.patient_id,
        doctor_id=doctor.id,
        appointment_date=data.appointment_date,
        symptoms=getattr(data, "symptoms", None) or getattr(data, "reason", None),
        status="BOOKED"
    )

    db.add(appointment)
    db.commit()
    db.refresh(appointment)

    create_notification(
        db,
        patient.user_id,
        "Appointment Booked",
        "Your appointment has been booked successfully."
    )

    create_audit_log(
        db,
        current_user.id,
        "CREATE",
        "APPOINTMENT"
    )
    return appointment

def get_all_appointments(db, current_user=None):
    if current_user is not None and str(current_user.role).lower() == "patient":
        patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
        if not patient:
            return []
        return db.query(Appointment).filter(Appointment.patient_id == patient.id).all()
    return db.query(Appointment).all()

def get_appointment_by_id(appointment_id, db, current_user=None):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return appointment

def reschedule_appointment(appointment_id,data,db,current_user):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    duplicate = db.query(Appointment).filter(Appointment.doctor_id ==appointment.doctor_id,Appointment.appointment_date ==data.appointment_date).first()

    if duplicate:
        raise HTTPException(status_code=400, detail="Slot already booked")

    appointment.appointment_date = (data.appointment_date)
    db.commit()

    create_audit_log(
        db,
        current_user.id,
        "UPDATE",
        "APPOINTMENT"
    )
    return appointment

def cancel_appointment(appointment_id, db, current_user):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = "CANCELLED"
    db.commit()

    create_audit_log(
        db, 
        current_user.id,
        "CANCEL",
        "APPOINTMENT"
    )
    return {"Info": "Appointment Cancelled"}
