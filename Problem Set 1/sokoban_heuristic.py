from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented

# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal


def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

# Done: Import any modules and write any functions you want to use
# My-Comment: No Import is needed


def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    # Done: ADD YOUR CODE HERE
    # IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    # NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function

    # My-Comment: I used the cache to store the number of goals in each wall and to cache the state calculated before
    # My-Comment: Initialize the cache for storing computed values
    cache = problem.cache()

    # My-Comment: Check if the current state is the goal state
    if problem.is_goal(state):
        return 0.0

    # My-Comment: Check if the state is already in the cache
    if state in cache:
        return cache[state]
    
    # Calculate how many goal in on wall and cache it
    if 'y1' not in cache:
        counter = sum([1 for x in range(1, state.layout.width - 1) if Point(x, 1) in state.layout.goals])
        cache['y1'] = counter

    if 'y2' not in cache:
        counter = sum([1 for x in range(1, state.layout.width - 1) if Point(x, state.layout.height - 2) in state.layout.goals])
        cache['y2'] = counter

    if 'x1' not in cache:
        counter = sum([1 for y in range(1, state.layout.height - 1) if Point(1, y) in state.layout.goals])
        cache['x1'] = counter

    if 'x2' not in cache:
        counter = sum([1 for y in range(1, state.layout.height - 1) if Point(state.layout.width - 2, y) in state.layout.goals])
        cache['x2'] = counter

    # My-Comment: check for deadlocks
    if deadlocked(state, problem):
        # My-Comment: Give it inf to put it away to decrease the expanded nodes
        heuristic_value = float('inf')
        # My-Comment: Store the computed value in the cache for future reference
        cache[state] = heuristic_value
        return heuristic_value

    # My-Comment: Compute the strong heuristic
    heuristic_value = compute_heuristic(problem, state)

    # My-Comment: Store the computed value in the cache for future reference
    cache[state] = heuristic_value
    return heuristic_value
    # NotImplemented()


def compute_heuristic(problem: SokobanProblem, state: SokobanState) -> float:

    # My-Comment: weak heuristic added to it the distances of each crate to its closest goal
    distance = weak_heuristic(problem, state) + sum(min(manhattan_distance(crate, goal)
                                                        for goal in problem.layout.goals) for crate in state.crates)
    return distance


def deadlocked(state: SokobanState, problem: SokobanProblem) -> bool:
    """
    #My-Comment:
    Check if the state is deadlocked.
    A state is deadlocked if there is a crate that cannot be moved to a goal.
    """
    # Check if there is a crate that is not on a goal
    counter_crates_y1 = 0
    counter_crates_y2 = 0
    counter_crates_x1 = 0
    counter_crates_x2 = 0
    # My-Comment: Check deadlocks for crates that is not on a goal
    for crate in state.crates:
        if crate not in state.layout.goals:
            # My-Comment: Check if the crate is deadlocked
            if is_deadlocked(state, crate):
                return True
            
        if crate.x == 1:
            counter_crates_x1 += 1
        if crate.x == (state.layout.width - 2):
            counter_crates_x2 += 1
        if crate.y == 1:
            counter_crates_y1 += 1
        if crate.y == (state.layout.height - 2):
            counter_crates_y2 += 1
            

    cache = problem.cache()
    # Check if number of goals is less than number of crates on each side walls
    if cache['y1'] < counter_crates_y1 or cache['y2'] < counter_crates_y2 or cache['x1'] < counter_crates_x1 or cache['x2'] < counter_crates_x2:
        return True

    return False


def is_deadlocked(state: SokobanState, crate: Point) -> bool:
    """
    #My-Comment:
    Check if the crate is deadlocked.
    A crate is deadlocked if it cannot be moved to a goal.
    """
    # My-Comment: Check if the crate is in a corner
    if is_corner(state, crate):
        return True

    # My-Comment: Check if the crate is on a wall side and stuck
    if is_on_wall(state, crate):
        return True

    return False


def is_corner(state: SokobanState, crate: Point) -> bool:
    """
    #My-Comment:
    Check if the crate is in a corner.
    A crate is in a corner if it has a wall in 2 adjacent directions.
    """
    # My-Comment: Check all four corners around the crate
    directions = [Direction.UP, Direction.LEFT,
                  Direction.DOWN, Direction.RIGHT]
    for i in range(4):
        dir1 = directions[i]
        # My-Comment: Get the next direction in the list, wrapping around to the start
        dir2 = directions[(i+1) % 4]
        if crate + dir1.to_vector() not in state.layout.walkable and crate + dir2.to_vector() not in state.layout.walkable:
            return True
        
    return False


def is_on_wall(state: SokobanState, crate: Point) -> bool:
    """
    #My-Comment:
    Check if the crate is on a wall side and stuck.
    A crate is on a wall if it is stuck due to other crate or ther is no goal on this wall then deadlock.
    """
    # My-Comment: Check if the crate is on a side of the grid
    if not is_corridor_of_side(state, crate):
        return False
        
    # My-Comment: Check if there is a wall on one side of the corridor and crate in one of the adjacent side
    if is_wall_on_one_side_and_stuck(state, crate):
        return True


    # My-Comment: Check if there is a wall on one side of the corridor and there is no goal
    if is_wall_on_one_side(state, crate):
        return True

    return False


def is_wall_on_one_side_and_stuck(state: SokobanState, crate: Point) -> bool:
    """
    #My-Comment:
    Check if there is a wall on one side of the corridor and crate in one of the adjacent side.
    """
    # My-Comment: Check if the crate is in the top corridor
    if crate.y == 1:
        # My-Comment: check if there is another crate on the right or left to it
        if crate + Direction.RIGHT.to_vector() in state.crates or crate + Direction.LEFT.to_vector() in state.crates:
            return True

    # My-Comment: Check if the crate is in the bottom corridor
    if crate.y == (state.layout.height - 2):
        # My-Comment: check if there is another crate on the right or left to it
        if crate + Direction.RIGHT.to_vector() in state.crates or crate + Direction.LEFT.to_vector() in state.crates:
            return True

    # My-Comment: Check if the crate is in the left corridor
    if crate.x == 1:
        # My-Comment: check if there is another crate on the top or bottom to it
        if crate + Direction.UP.to_vector() in state.crates or crate + Direction.DOWN.to_vector() in state.crates:
            return True

    # My-Comment: Check if the crate is in the right corridor
    if crate.x == (state.layout.width - 2):
        # My-Comment: check if there is another crate on the top or bottom to it
        if crate + Direction.UP.to_vector() in state.crates or crate + Direction.DOWN.to_vector() in state.crates:
            return True

    return False


def is_corridor_of_side(state: SokobanState, crate: Point) -> bool:
    """
    # My-Comment
    Check if the crate is on a side of the grid.
    """
    # My-Comment Check if the crate is in the top corridor
    if crate.y == 1:
        return True

    # My-Comment Check if the crate is in the bottom corridor
    if crate.y == (state.layout.height - 2):
        return True

    # My-Comment Check if the crate is in the left corridor
    if crate.x == 1:
        return True

    # My-Comment Check if the crate is in the right corridor
    if crate.x == (state.layout.width - 2):
        return True

    return False


def is_wall_on_one_side(state: SokobanState, crate: Point) -> bool:
    """
    #My-Comment:
    Check if there is a wall on one side of the corridor and there is no goal.
    """
    # My-Comment: Check if the crate is in the top corridor
    if crate.y == 1:
        # My-Comment: check if there is goal on this line then return false
        for goal in state.layout.goals:
            if goal.y == 1:
                return False

    # My-Comment: Check if the crate is in the bottom corridor
    if crate.y == (state.layout.height - 2):
        # My-Comment: check if there is goal on this line then return false
        for goal in state.layout.goals:
            if goal.y == (state.layout.height - 2):
                return False

    # My-Comment: Check if the crate is in the left corridor
    if crate.x == 1:
        # My-Comment: check if there is goal on this line then return false
        for goal in state.layout.goals:
            if goal.x == 1:
                return False

    # My-Comment: Check if the crate is in the right corridor
    if crate.x == (state.layout.width - 2):
        # My-Comment: check if there is goal on this line then return false
        for goal in state.layout.goals:
            if goal.x == (state.layout.width - 2):
                return False

    return True
