from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)
    payment_method = Column(String(50), nullable=False)
    payment_status = Column(String(50), default="Pending")
    transaction_id = Column(String(255), nullable=True)
