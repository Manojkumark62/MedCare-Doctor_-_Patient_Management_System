from sqlalchemy import Column, Integer, ForeignKey, DateTime
from database import Base
from datetime import datetime

class Admission(Base):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    admitted_at = Column(DateTime, default=datetime.utcnow)
    discharge_date = Column(DateTime, nullable=True)