from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from dependencies.roles import role_required
from services.report_service import daily_appointments, revenue_report, patient_statistics

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/appointments")
def appointments_report(db: Session = Depends(get_db), current_user=Depends(role_required(["ADMIN"]))):

    return daily_appointments(db)

@router.get("/revenue")
def revenue(db: Session = Depends(get_db), current_user=Depends(role_required(["ADMIN"]))):

    return revenue_report(db)

@router.get("/patients")
def stats(db: Session = Depends(get_db), current_user=Depends(role_required(["ADMIN"]))):

    return patient_statistics(db)
