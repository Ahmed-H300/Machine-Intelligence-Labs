from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

# Done: (Optional) Instead of Any, you can define a type for the parking state
# My-Comment: As the state will be the position of cars so it is better to be Tuple of points as it will defines position of cars
ParkingState = Tuple[Point]

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem


class ParkingProblem(Problem[ParkingState, ParkingAction]):
    # A set of points which indicate where a car can be (in other words, every position except walls).
    passages: Set[Point]
    # A tuple of points where state[i] is the position of car 'i'.
    cars: Tuple[Point]
    # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
    slots: Dict[Point, int]
    # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        # Done: ADD YOUR CODE HERE
        # My-Comment: The initial state will be the position of cars at the beginning is the initial state
        return self.cars
        # NotImplemented()

    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        # Done: ADD YOUR CODE HERE
        # My-Comment: check whether if this position in the parking slots
        # My-Comment: check whether all cars in it's position or not if one is not return false
        for car_i, car_point in enumerate(state):
            if not (car_point in self.slots) or car_i != self.slots[car_point]:
                return False
        return True
        # NotImplemented()

    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        # Done: ADD YOUR CODE HERE
        # My-Comment: The possible actions are the directions that the cars can move in
        # My-Comment: so i loop on every cars position try to move in the four directions
        # My-Comment: check if its is valid append it to the action list
        # My-Comment: self.passages has set of points which indicate where a car can be
        # My-Comment: And check if this place is not already occupied by a car
        actions = []
        for car_i, car_point in enumerate(state):
            for direction in Direction:
                new_point = car_point + direction.to_vector()
                if new_point in self.passages and new_point not in state:
                    actions.append((car_i, direction))
        return actions
        # NotImplemented()

    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        # Done: ADD YOUR CODE HERE
        # My-Comment: the new state is the state after applying the action
        # My-Comment: so i loop on every car in the state and check if it is the car that i want to move
        # My-Comment: if it is the car i want to move i move it in the direction of the action
        # My-Comment: if it is not the car i want to move i append it to the new state
        new_state = list(state)
        car_i, direction = action
        car_point = new_state[car_i]
        new_state[car_i] = car_point + direction.to_vector()
        return tuple(new_state)
        # NotImplemented()

    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        # Done: ADD YOUR CODE HERE
        # My-Comment: the cost is relative to the type of car A-> 26 till z --> 1
        # My-Comment: if car passes over other car parking slot cost is 100 + cost of moving
        car_i, direction = action
        car_point = state[car_i]
        new_car_point = car_point + direction.to_vector()
        cost = ord('Z') - ord('A') + 1 - car_i
        if new_car_point in self.slots and car_i != self.slots[new_car_point]:
            cost += 100
        return cost
        # NotImplemented()

     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages = set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip()
                                   for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position: index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
