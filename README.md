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
- GraphQL Application: http://localhost:8001/graphql
- OpenObserve UI: http://localhost:5080
  - Default credentials:
    - Email: admin@example.com
    - Password: Complexpass#123

## API Endpoints

### FastAPI REST Endpoints

1. Get Parking Status:
```bash
curl --location 'http://localhost:8000/parking/status'
```

2. Get Parking History:
```bash
curl --location 'http://localhost:8000/parking/history'
```

3. Enter Parking:
```bash
curl --location 'http://localhost:8000/parking/enter/1?vehicle_number=ABC123'
```

4. Exit Parking:
```bash
curl --location 'http://localhost:8000/parking/exit/1'
```

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

## GraphQL API Examples

### Queries

1. Get Parking Status:
```graphql
query {
  parkingStatus {
    totalSpots
    availableSpots
    occupiedSpots
  }
}
```

Curl command:
```bash
curl --location 'http://localhost:8001/graphql' \
--header 'Content-Type: application/json' \
--data '{"query":"{ parkingStatus { totalSpots availableSpots occupiedSpots } }","variables":{}}'
```

2. Get Parking History:
```graphql
query {
  parkingHistory {
    id
    vehicleNumber
    entryTime
    exitTime
    duration
    fee
  }
}
```

Curl command:
```bash
curl --location 'http://localhost:8001/graphql' \
--header 'Content-Type: application/json' \
--data '{"query":"{ parkingHistory { id vehicleNumber entryTime exitTime duration fee } }","variables":{}}'
```

### Mutations

1. Enter Parking:
```graphql
mutation {
  enterParking(vehicleNumber: "ABC123") {
    id
    vehicleNumber
    entryTime
  }
}
```

Curl command:
```bash
curl --location 'http://localhost:8001/graphql' \
--header 'Content-Type: application/json' \
--data '{"query":"mutation { enterParking(vehicleNumber: \"ABC123\") { id vehicleNumber entryTime } }","variables":{}}'
```

2. Exit Parking:
```graphql
mutation {
  exitParking(vehicleNumber: "ABC123") {
    id
    vehicleNumber
    entryTime
    exitTime
    duration
    fee
  }
}
```

Curl command:
```bash
curl --location 'http://localhost:8001/graphql' \
--header 'Content-Type: application/json' \
--data '{"query":"mutation { exitParking(vehicleNumber: \"ABC123\") { id vehicleNumber entryTime exitTime duration fee } }","variables":{}}'
``` 