from typing import Any, Set, Tuple
from grid import Grid
import utils

def locate(grid: Grid, item: Any) -> Set[Tuple[int,int]]:
    '''
    This function takes a 2D grid and an item
    It should return a list of (x, y) coordinates that specify the locations that contain the given item
    To know how to use the Grid class, see the file "grid.py"  
    '''
    #DONE: ADD YOUR CODE HERE
    # utils.NotImplemented()
    i, j = grid.height, grid.width
    locations = set()
    for x in range(i):
        for y in range(j):
            if grid[(y, x)] == item:
                locations.add((y, x))
    return locations

    