from typing import Any, Dict, List
import utils


def histogram(values: List[Any]) -> Dict[Any, int]:
    '''
    This function takes a list of values and returns a dictionary that contains the
    list elements alongside their frequency
    For example, if the values are [3,5,3] then the result should be {3:2, 5:1} 
    since 3 appears twice while 5 appears once 
    '''
    #DONE: ADD YOUR CODE HERE
    # utils.NotImplemented()
    hist = {}
    for i in values:
        if i in hist:
            hist[i] += 1
        else:
            hist[i] = 1

    # another solution
    # [hist.update({i: hist.get(i, 0) + 1}) for i in values]

    return hist
