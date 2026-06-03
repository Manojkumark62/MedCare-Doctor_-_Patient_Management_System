from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.prescriptions import Prescription
from models.prescription_items import PrescriptionItem
from models.appointments import Appointment
from services.billing_service import generate_bill
from services.audit_service import create_audit_log

def create_prescription(data, db: Session, current_user):
    appointment = db.query(Appointment).filter(Appointment.id ==data.appointment_id).first()

    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    prescription = Prescription(
        appointment_id=data.appointment_id,
        patient_id=data.patient_id,
        doctor_id=data.doctor_id,
        notes=data.notes)

    db.add(prescription)
    db.commit()
    db.refresh(prescription)

    for medicine in data.medicines:

        item = PrescriptionItem(
            prescription_id=prescription.id,
            medicine_name=medicine.medicine_name,
            dosage=medicine.dosage,
            duration=medicine.duration)

        db.add(item)
    db.commit()

    appointment.status = "COMPLETED"
    db.commit()

    bill = generate_bill(appointment, db)

    create_audit_log(
        db,
        current_user.id,
        "CREATE",
        "PRESCRIPTION"
    )

    return {
        "prescription": prescription.id,
        "bill_id": bill.id,
        "message": "Prescription created"}

def get_prescriptions(patient_id, db):

    return db.query(Prescription).filter(Prescription.patient_id == patient_id).all()
