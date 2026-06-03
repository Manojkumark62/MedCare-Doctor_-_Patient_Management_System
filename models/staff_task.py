from sqlalchemy import Column, Integer, String
from database import Base

class StaffTask(Base):
    __tablename__ = "staff_tasks"

    id = Column(Integer, primary_key=True, index=True)
    assigned_to = Column(Integer)
    task_title = Column(String(255), nullable=False)
    status = Column(String(50), default="Pending")
