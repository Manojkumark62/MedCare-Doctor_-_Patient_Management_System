import uuid
from fastapi import HTTPException
from models.bills import Bill
from models.payments import Payment
from models.patients import Patient
from models.appointments import Appointment
from services.notification_service import create_notification
from services.audit_service import create_audit_log

def process_payment(data, db, current_user):
    bill = db.query(Bill).filter(Bill.id == data.bill_id).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    if bill.status == "PAID":
        raise HTTPException(status_code=400, detail="Bill already paid")

    transaction_id = str(uuid.uuid4())

    payment = Payment(
        bill_id=bill.id,
        payment_method=data.payment_method,
        payment_status="SUCCESS",
        transaction_id=transaction_id)

    db.add(payment)
    bill.status = "PAID"

    db.commit()
    db.refresh(payment)

    patient = db.query(Patient).filter(Patient.id == bill.patient_id).first()

    if patient:

        create_notification(db, patient.user_id, "Payment Successful",
            f"Payment completed. Transaction ID: {transaction_id}")

    create_audit_log(
        db,
        current_user.id,
        "PAYMENT",
        "BILL")

    return {
        "message": "Payment Successful",
        "transaction_id": transaction_id}