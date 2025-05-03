# Parking Lot API with OpenTelemetry and OpenObserve

This is a FastAPI-based parking lot management system with PostgreSQL database, OpenTelemetry for observability, and OpenObserve for visualization.

## Features

- Park and exit vehicles
- Track parking spot status
- Monitor system performance with OpenTelemetry
- Visualize metrics and traces with OpenObserve

## Prerequisites

- Docker
- Docker Compose

## Getting Started

1. Clone the repository
2. Run the application:
   ```bash
   docker-compose up --build
   ```

## Accessing the Services

- FastAPI Application: http://localhost:8000
- OpenObserve UI: http://localhost:5080
  - Default credentials:
    - Email: admin@example.com
    - Password: Complexpass#123

## API Endpoints

- `POST /parking/enter/{spot_number}` - Park a vehicle
  - Query parameter: `vehicle_number`
- `POST /parking/exit/{spot_number}` - Exit a vehicle
- `GET /parking/status` - Get current parking status

## Architecture

- FastAPI application with SQLAlchemy ORM
- PostgreSQL database
- OpenTelemetry Collector for metrics and traces
- OpenObserve for visualization

## Monitoring

The application is instrumented with OpenTelemetry, which sends:
- Traces for API calls
- Metrics for system performance
- Logs for application events

All this data is collected by the OpenTelemetry Collector and forwarded to OpenObserve for visualization. 