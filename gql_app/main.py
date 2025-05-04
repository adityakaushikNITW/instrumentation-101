from ariadne import make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from ariadne.asgi import GraphQL
from ariadne.asgi.handlers import GraphQLHTTPHandler
from gql_app.core.telemetry import setup_telemetry, GraphQLMetricsExtension
from gql_app.db.database import engine
from gql_app.db.models import Base
from gql_app.api.resolvers import (
    resolve_parking_status,
    resolve_parking_history,
    resolve_enter_parking,
    resolve_exit_parking
)
import logging

# Setup telemetry
setup_telemetry()

# Get logger
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Load schema
type_defs = load_schema_from_path("gql_app/api/schema.py")

# Create type definitions
query = QueryType()
mutation = MutationType()
parking_status = ObjectType("ParkingStatus")
parking_record = ObjectType("ParkingRecord")

# Set up resolvers
query.set_field("parkingStatus", resolve_parking_status)
query.set_field("parkingHistory", resolve_parking_history)
mutation.set_field("enterParking", resolve_enter_parking)
mutation.set_field("exitParking", resolve_exit_parking)

# Create executable schema
schema = make_executable_schema(
    type_defs,
    query,
    mutation,
    parking_status,
    parking_record
)

# Create HTTP handler with metrics extension
http_handler = GraphQLHTTPHandler(extensions=[GraphQLMetricsExtension])

# Create ASGI application
app = GraphQL(schema, debug=True, http_handler=http_handler) 