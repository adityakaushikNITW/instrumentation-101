from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ParkingRecord(Base):
    __tablename__ = "parking_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_number = Column(String, index=True)
    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)
    status = Column(String, default="PARKED") 