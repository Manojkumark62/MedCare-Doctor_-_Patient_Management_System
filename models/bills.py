from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, DECIMAL
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String(50), default="Unpaid")
    created_at = Column(DateTime, default=datetime.utcnow)