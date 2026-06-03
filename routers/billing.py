from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from dependencies.roles import role_required
from schemas.billing import PaymentCreate, BillResponse
from services.payment_service import process_payment
from services.billing_service import get_bill as get_bill_service

router = APIRouter(prefix="/billing", tags=["Billing"])

@router.post("/payment")
def payment(data: PaymentCreate, db: Session = Depends(get_db), current_user=Depends(role_required(["ADMIN", "RECEPTIONIST"]))):
    return process_payment(data, db, current_user)

@router.get("/bill/{bill_id}", response_model=BillResponse)
def get_bill_route(bill_id: int, db: Session = Depends(get_db), current_user=Depends(role_required(["ADMIN", "RECEPTIONIST", "PATIENT"]))):
    return get_bill_service(db, bill_id, current_user)