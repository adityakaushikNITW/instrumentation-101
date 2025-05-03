type Query {
    parkingStatus: ParkingStatus!
    parkingHistory: [ParkingRecord!]!
}

type Mutation {
    enterParking(vehicleNumber: String!): ParkingRecord!
    exitParking(vehicleNumber: String!): ParkingRecord!
}

type ParkingStatus {
    totalSpots: Int!
    availableSpots: Int!
    occupiedSpots: Int!
}

type ParkingRecord {
    id: ID!
    vehicleNumber: String!
    entryTime: String!
    exitTime: String
    status: String!
} 