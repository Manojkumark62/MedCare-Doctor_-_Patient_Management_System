from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class Specialization(Base):
    __tablename__ = "specializations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)

    doctors = relationship("Doctor", back_populates="specialization")
