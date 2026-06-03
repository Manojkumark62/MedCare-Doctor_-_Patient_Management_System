from pydantic import BaseModel

class PaymentCreate(BaseModel):
    bill_id: int
    payment_method: str

class BillResponse(BaseModel):
    id: int
    patient_id: int
    appointment_id: int
    total_amount: float
    status: str

    class Config:
        from_attributes = True
