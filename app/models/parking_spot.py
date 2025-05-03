from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.db.database import Base

class ParkingSpot(Base):
    __tablename__ = "parking_spots"

    id = Column(Integer, primary_key=True, index=True)
    spot_number = Column(String, unique=True, index=True)
    is_occupied = Column(Boolean, default=False)
    vehicle_number = Column(String, nullable=True)
    entry_time = Column(DateTime, nullable=True)
    exit_time = Column(DateTime, nullable=True) 