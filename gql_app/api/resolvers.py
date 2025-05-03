from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from gql_app.db.models import ParkingRecord
from gql_app.db.database import get_db
from typing import List
import logging
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

logger = logging.getLogger(__name__)

def resolve_parking_status(*_):
    db = next(get_db())
    try:
        total_spots = 100  # Assuming 100 parking spots
        occupied_spots = db.query(func.count(ParkingRecord.id)).filter(
            ParkingRecord.exit_time == None
        ).scalar()
        available_spots = total_spots - occupied_spots
        
        logger.info(f"Parking status checked - Available: {available_spots}, Occupied: {occupied_spots}")
        
        return {
            "totalSpots": total_spots,
            "availableSpots": available_spots,
            "occupiedSpots": occupied_spots
        }
    finally:
        db.close()

def resolve_parking_history(*_):
    db = next(get_db())
    try:
        records = db.query(ParkingRecord).order_by(ParkingRecord.entry_time.desc()).all()
        logger.info(f"Retrieved {len(records)} parking records")
        return records
    finally:
        db.close()

def resolve_enter_parking(_, info, vehicle_number: str):
    db = next(get_db())
    try:
        # Check if vehicle is already parked
        existing_record = db.query(ParkingRecord).filter(
            ParkingRecord.vehicle_number == vehicle_number,
            ParkingRecord.exit_time == None
        ).first()
        
        if existing_record:
            logger.warning(f"Vehicle {vehicle_number} already parked")
            raise Exception("Vehicle is already parked")
        
        # Check if parking is full
        occupied_spots = db.query(func.count(ParkingRecord.id)).filter(
            ParkingRecord.exit_time == None
        ).scalar()
        
        if occupied_spots >= 100:  # Assuming 100 parking spots
            logger.warning("Parking lot is full")
            raise Exception("Parking lot is full")
        
        # Create new parking record
        record = ParkingRecord(
            vehicle_number=vehicle_number,
            entry_time=datetime.utcnow(),
            status="PARKED"
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        
        logger.info(f"Vehicle {vehicle_number} entered parking")
        return record
    finally:
        db.close()

def resolve_exit_parking(_, info, vehicle_number: str):
    db = next(get_db())
    try:
        record = db.query(ParkingRecord).filter(
            ParkingRecord.vehicle_number == vehicle_number,
            ParkingRecord.exit_time == None
        ).first()
        
        if not record:
            logger.warning(f"Vehicle {vehicle_number} not found in parking")
            raise Exception("Vehicle not found in parking")
        
        record.exit_time = datetime.utcnow()
        record.status = "EXITED"
        db.commit()
        db.refresh(record)
        
        logger.info(f"Vehicle {vehicle_number} exited parking")
        return record
    finally:
        db.close() 