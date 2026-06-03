from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class AppointmentSlot(Base):
    __tablename__ = "appointment_slots"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    availability_status = Column(Boolean, default=True)