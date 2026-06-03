from fastapi import HTTPException
from models.bills import Bill
from models.doctors import Doctor
from models.patients import Patient


def generate_bill(appointment, db):
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    bill = Bill(patient_id=appointment.patient_id, appointment_id=appointment.id, total_amount=doctor.consultation_fee, status="PENDING")

    db.add(bill)
    db.commit()
    db.refresh(bill)

    return bill


def get_bill(db, bill_id: int, current_user=None):
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    if current_user is not None and str(current_user.role).lower() == "patient":
        patient = db.query(Patient).filter(Patient.id == bill.patient_id).first()
        if not patient or patient.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")

    return bill