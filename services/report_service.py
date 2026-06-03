from sqlalchemy import func
from models.appointments import Appointment
from models.bills import Bill
from models.patients import Patient

def daily_appointments(db):

    total = db.query(
        Appointment
    ).count()

    return {
        "total_appointments": total
    }


def revenue_report(db):

    revenue = db.query(
        func.sum(Bill.total_amount)
    ).filter(
        Bill.status == "PAID"
    ).scalar()

    return {
        "revenue": revenue or 0
    }


def patient_statistics(db):

    total_patients = db.query(
        Patient
    ).count()

    total_bills = db.query(
        Bill
    ).count()

    return {
        "patients": total_patients,
        "bills": total_bills}