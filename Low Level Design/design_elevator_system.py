# Elevator System

"""
Design a simple in-memory simulation of a bank of elevators serving a range of floors
processing hall and cabin requests in discrete time steps.

"""

# 1. Requirements

"""
# 1a. Functional Requirements

1. A user should be able to take an elevator car from one floor to another.
2. The same elevator principle should work in any of the elevator cars.
3. The dispatch policy should be: 'the nearest car policy'.
4. The optimization/minimization policy should be: 'minimalization of user-time'.

# 1b. Non-functional Requirements

1. Scalability (Assumptions about application):
    - up to 20 elevator cars in suite.
    - minFloor < maxFloor, and a range <= 100.
    - max user wait time for a car <= 30s
    - number of requests at any time <= 1000
2. High avalability of the system.

"""

# 2. Core Entities -> (Nouns of our application)

"""
1. Elevator (car)
2. Elevator controller
3. Request

"""

# 3. System Interface (API) -> (Contracts with our users - returns our Nouns)

"""
1. Elevator
    - id: int
    - minFloor: int
    - maxFloor: int
    - current_floor: int
    - state: ElevatorStateEnum
    - direction: DirectionEnum
    - requests: Request[]

    + addRequest(req: Request): void
    + step(): void

2. Elevator controller
    - numOfElevators: int
    - minFloor: int
    - maxFloor: int
    - elevators: Elevator[]
    
    + requestElevator(req: Request): void
    + stepAllElevators(): void
    + processRequests(cmds: str[]): void
    + getElevatorFloor(eid: int): int
    + getElevatorState(eid: int): ElevatorStateEnum
    + getElevatorDirection(eid: int): DirectionEnum

3. Request
    - floor: int
    - direction: DirectionEnum
"""

# 4. Low-level Design

from enum import Enum
from threading import Lock

class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"

class ElevatorState(Enum):
    MOVING = "MOVING"
    STOPPED = "STOPPED"
    DOOR_OPEN = "DOOR_OPEN"

class Request:
    def __init__(self, floor: int, direction: Direction = None):
        self.floor = floor
        self.direction = direction

class Elevator:
    def __init__(self, eid: int, min_floor: int, max_floor: int):
        self.eid = eid
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.current_floor = min_floor
        self.state = ElevatorState.STOPPED
        self.direction = Direction.IDLE
        self.requests: list[Request] = []
        self.lock = Lock()

    def add_request(self, req: Request):
        with self.lock:
            self.requests.append(req)
            self.requests.sort(key=lambda r: abs(r.floor - self.current_floor))

    def step(self):
        with self.lock:
            self._check_request_empty()
            
            target = self.requests[0].floor

            if target > self.current_floor:
                self.direction = Direction.UP
                self.current_floor += 1
                self.state = ElevatorState.MOVING
            elif target < self.current_floor:
                self.direction = Direction.DOWN
                self.current_floor -= 1
                self.state = ElevatorState.MOVING
            else:
                self._open_doors()
                self.requests.pop(0)
                self._check_request_empty()

    def _check_request_empty(self):
        if not self.requests:
            self.state = ElevatorState.STOPPED
            self.direction = Direction.IDLE
            return None
    def _open_doors(self):
        self.state = ElevatorState.DOOR_OPEN
        self.state = ElevatorState.STOPPED


class ElevatorController:
    def __init__(self, num_elevators: int, min_floor: int, max_floor: int):
        self.elevators: list[Elevator] = [
            Elevator(eid=i, min_floor=min_floor, max_floor=max_floor) 
            for i in range(num_elevators)
        ]
        self.lock = Lock()
    
    def request_elevator(self, req: Request):
        with self.lock:
            chosen_elevator = min(
                self.elevators, 
                key=lambda e: abs(e.current_floor - req.floor)
            )
            chosen_elevator.add_request(req)
    def step_all_elevators(self):
        for elevator in self.elevators:
            elevator.step()


    def process_requests(self, cmds: list[str]):
        for cmd in cmds:
            request, floor, direction = cmd.split()
            if request == 'REQUEST':
                floor = int(floor)
                direction = Direction[direction]
                self.request_elevator(Request(floor, direction))
        while any(e.requests for e in self.elevators):
            self.step_all_elevators()

    def get_elevator_floor(self, eid: int) -> int:
        return self.elevators[eid].current_floor

    def get_elevator_state(self, eid: int) -> ElevatorState:
        return self.elevators[eid].state

    def get_elevator_direction(self, eid: int) -> Direction:
        return self.elevators[eid].direction


# 5. Dive-Dive(if any)