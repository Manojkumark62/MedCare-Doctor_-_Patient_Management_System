from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from database import Base
from sqlalchemy.orm import relationship

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    #department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    #specialization_id = Column(Integer, ForeignKey("specializations.id"), nullable=False)
    experience = Column(Integer, nullable=False)
    consultation_fee = Column(DECIMAL(10, 2), nullable=False)
    
    user = relationship("User", back_populates="doctor")
    #department = relationship("Department", back_populates="doctor")
    #specialization = relationship("Specialization", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    medical_records = relationship("MedicalRecord", back_populates="doctor")