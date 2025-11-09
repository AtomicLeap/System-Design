# Parking Lot System

"""
Design a Parking Lot system.
"""

# 1. Requirements

"""
# 1a. Functional Requirements

1. A user should be able to view available parking spots.
2. A user should be able to request a parking spot by vehicle size and registration number.
3. A user should be assigned a parking spot and the spot removed from list of available spots.
4. A user should be able to exit a parking spot and the spot listed again in list of available spots.

# 1b. Non-functional Requirements

1. Scalability (Assumptions about application):
    - multi-level parking lot with up to 10 levels.
    - each level has same amount of parking spots.
    - each level parking distributed as follows: SMALL - 20%, MEDIUM - 50%, LARGE - 20% and XLARGE - 10%. 
2. Parking spots for vehicles of sizes, SMALL (S), MEDIUM (M), LARGE (L) AND EXTRALARGE(XL).
3. Vehicles can only park in spots that corresponds to vehicle size only.
    - Motorcycles -> SMALL, Car -> MEDIUM, Bus -> LARGE, and Truck -> XLARGE.
4. High avalability for viewing spots and high consistency for assigning spots.

"""

# 2. Core Entities -> (Nouns of our application)

"""
1. Parking lot
2. Parking Level
2. Parking spot
3. Vehicle

"""

# 3. System Interface (API) -> (Contracts with our users - returns our Nouns)

"""
1. Vehicle
    - plateNumber: str
    - type: VehicleTypeEnum

2. Parking Spot
    - id: int
    - size: SpotSizeEnum

    + isAvailable(): boolean
    + canFitVehicle(vehicle: Vehicle): boolean
    + parkVehicle(vehicle: Vehicle): boolean
    + removeVehicle(): Vehicle | None

3. Parking Level
    - levelId: int
    - numOfSpots: int

    - spots: Spot[]

    + initializeSpot(numOfSpots: int)
    + findAvailableSpot(vehicle: VehicleTypeEnum)
    + getAvailableSpotsCount(vehicle: VehicleTypeEnum)

4. Parking Lot
    - numOfLevels: int
    - numOfSpotsPerLevel: int

    - levels: ParkingLevel[]
    - occupied: dict[vehiclePlateNumber: str, spotId: str]
    - SpotMap: dict[spotId: str, ParkingSpot]

    + parkVehicle(vehicle: Vehicle): boolean
    + removeVehicle(vehiclePlateNumber: str): boolean
    + getAvailableSpots(vehicleType: VehicleTypeEnum): int

"""

# 4. Low-level Design

from enum import Enum

class VehicleType(Enum):
    MOTORCYCLE = "Motorcycle"
    CAR = "Car"
    BUS = "Bus"
    TRUCK = "Truck"

class SpotSize(Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"
    XLARGE = "XLarge"

class Vehicle:
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self.license_plate = license_plate
        self.vehicle_type = vehicle_type

class ParkingSpot:
    def __init__(self, spot_id: str, size: SpotSize):
        self.spot_id = spot_id
        self.size = size
        self.vehicle: Vehicle | None = None

    def is_available(self) -> bool:
        return self.vehicle is None

    def can_fit_vehicle(self, vehicle: Vehicle) -> bool:
        # Vehicles can only park in their exact size match
        size_map = {
            VehicleType.MOTORCYCLE: SpotSize.SMALL,
            VehicleType.CAR: SpotSize.MEDIUM,
            VehicleType.BUS: SpotSize.LARGE,
            VehicleType.TRUCK: SpotSize.EXTRALARGE
        }
        return self.size == size_map[vehicle.vehicle_type]

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        if self.is_available() and self.can_fit_vehicle(vehicle):
            self.vehicle = vehicle
            return True
        return False

    def remove_vehicle(self) -> Vehicle | None:
        vehicle = self.vehicle
        self.vehicle = None
        return vehicle 

class ParkingLevel:
    def __init__(self, level_id: str, num_spots: int):
        self.level_id = level_id
        self.spots: list[ParkingSpot] = []
        self._initialize_spots(num_spots)

    def _initialize_spots(self, num_spots: int):
        num_small = int(num_spots * 0.2)
        num_medium = int(num_spots * 0.5)
        num_large = int(num_spots * 0.2)
        num_xlarge = int(num_spots * 0.1)
        idx = 1
        for _ in range(num_small):
            self.spots.append(ParkingSpot(f"LEVEL_{self.level_id}_SPOT_{idx}", SpotSize.SMALL))
            idx += 1
        for _ in range(num_medium):
            self.spots.append(ParkingSpot(f"LEVEL_{self.level_id}_SPOT_{idx}", SpotSize.MEDIUM))
            idx += 1
        for _ in range(num_large):
            self.spots.append(ParkingSpot(f"LEVEL_{self.level_id}_SPOT_{idx}", SpotSize.LARGE))
            idx += 1
        for _ in range(num_xlarge):
            self.spots.append(ParkingSpot(f"LEVEL_{self.level_id}_SPOT_{idx}", SpotSize.XLARGE))
            idx += 1

    def find_available_spot(self, vehicle: Vehicle) -> ParkingSpot | None:
        for spot in self.spots:
            if spot.isAvailable() and spot.canFitVehicle(vehicle):
                return spot
        return None

    def get_available_spots_count(self, vehicle_type: VehicleType) -> int:
        dummy = Vehicle("", vehicle_type)
        return sum(
            1
            for spot in self.spots
            if spot.isAvailable() and spot.canFitVehicle(dummy)
        )

class ParkingLot:
    def __init__(self, num_levels: int, spots_per_level: int):
        self.levels: list[ParkingLevel] = [
            ParkingLevel(f"LEVEL_{i+1}", spots_per_level) for i in range(num_levels)
        ]
        # Tracks: license_plate → spot_id
        self.occupied: dict[str, str] = {}
        # NEW: Tracks: spot_id → ParkingSpot reference for O(1) lookup
        self.spot_map: dict[str, ParkingSpot] = {}
        
        # Build the spot_map
        for level in self.levels:
            for spot in level.spots:
                self.spot_map[spot.spot_id] = spot

    def park_vehicle(self, vehicle: Vehicle) -> bool:
        if vehicle.license_plate in self.occupied:
            return False  # already parked
        for level in self.levels:
            spot = level.find_available_spot(vehicle)
            if spot and spot.park_vehicle(vehicle):
                self.occupied[vehicle.license_plate] = spot.spot_id
                return True
        return False

    def remove_vehicle(self, license_plate: str) -> bool:
        spot_id = self.occupied.get(license_plate)
        if not spot_id:
            return False
        
        spot = self.spot_map.get(spot_id)
        if spot and spot.vehicle and spot.vehicle.license_plate == license_plate:
            spot.removeVehicle()
            del self.occupied[license_plate]
            return True
        return False

    def get_available_spots(self, vehicle_type: VehicleType) -> int:
        return sum(level.get_available_spots_count(vehicle_type) for level in self.levels)
