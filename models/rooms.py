from sqlalchemy import Column, Integer, String
from database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(50), unique=True, nullable=False)
    room_type = Column(String(50), nullable=False)
    status = Column(String(50), default="Available")