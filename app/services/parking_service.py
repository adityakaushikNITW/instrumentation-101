from datetime import datetime
from sqlalchemy.orm import Session
from app.models.parking_spot import ParkingSpot
from fastapi import HTTPException

class ParkingService:
    @staticmethod
    def enter_parking(spot_number: str, vehicle_number: str, db: Session):
        spot = db.query(ParkingSpot).filter(ParkingSpot.spot_number == spot_number).first()
        if not spot:
            spot = ParkingSpot(spot_number=spot_number)
            db.add(spot)
        
        if spot.is_occupied:
            raise HTTPException(status_code=400, detail="Spot is already occupied")
        
        spot.is_occupied = True
        spot.vehicle_number = vehicle_number
        spot.entry_time = datetime.utcnow()
        db.commit()
        return {"message": f"Vehicle {vehicle_number} parked in spot {spot_number}"}

    @staticmethod
    def exit_parking(spot_number: str, db: Session):
        spot = db.query(ParkingSpot).filter(ParkingSpot.spot_number == spot_number).first()
        if not spot:
            raise HTTPException(status_code=404, detail="Spot not found")
        
        if not spot.is_occupied:
            raise HTTPException(status_code=400, detail="Spot is already empty")
        
        spot.is_occupied = False
        spot.exit_time = datetime.utcnow()
        db.commit()
        return {"message": f"Vehicle {spot.vehicle_number} exited spot {spot_number}"}

    @staticmethod
    def get_parking_status(db: Session):
        spots = db.query(ParkingSpot).all()
        return {
            "total_spots": len(spots),
            "occupied_spots": sum(1 for spot in spots if spot.is_occupied),
            "available_spots": sum(1 for spot in spots if not spot.is_occupied),
            "spots": [{
                "spot_number": spot.spot_number,
                "is_occupied": spot.is_occupied,
                "vehicle_number": spot.vehicle_number,
                "entry_time": spot.entry_time,
                "exit_time": spot.exit_time
            } for spot in spots]
        } 