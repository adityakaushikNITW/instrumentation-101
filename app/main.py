from fastapi import FastAPI, HTTPException
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from app.core.telemetry import setup_telemetry
from app.db.database import engine, Base
from app.api.parking_routes import router
from opentelemetry import metrics, trace
import logging

# Get logger
logger = logging.getLogger(__name__)

def create_application() -> FastAPI:
    # Initialize OpenTelemetry
    setup_telemetry()

    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Instrument SQLAlchemy
    SQLAlchemyInstrumentor().instrument(engine=engine)

    # Create FastAPI app
    app = FastAPI(title="Parking Lot API")

    # Include routers
    app.include_router(router)

    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)

    return app

app = create_application()

@app.get("/")
async def root():
    # Log an info message
    logger.info("Root endpoint accessed")

    # Get meter and tracer
    meter = metrics.get_meter(__name__)
    tracer = trace.get_tracer(__name__)
        # Create metrics
    parking_requests = meter.create_counter(
        "parking_requests_total",
        description="Total number of parking requests"
    )
    # Increment the counter
    parking_requests.add(1)
    
    # Create a span
    with tracer.start_as_current_span("root_endpoint"):
        return {"message": "Welcome to the Parking Lot API"}
