from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.parking_service import ParkingService
from opentelemetry import trace

router = APIRouter(prefix="/parking", tags=["parking"])

@router.post("/enter/{spot_number}")
async def enter_parking(spot_number: str, vehicle_number: str, db: Session = Depends(get_db)):
    with trace.get_tracer(__name__).start_as_current_span("enter_parking") as span:
        return ParkingService.enter_parking(spot_number, vehicle_number, db)

@router.post("/exit/{spot_number}")
async def exit_parking(spot_number: str, db: Session = Depends(get_db)):
    with trace.get_tracer(__name__).start_as_current_span("exit_parking") as span:
        return ParkingService.exit_parking(spot_number, db)

@router.get("/status")
async def get_parking_status(db: Session = Depends(get_db)):
    with trace.get_tracer(__name__).start_as_current_span("get_parking_status") as span:
        return ParkingService.get_parking_status(db) 