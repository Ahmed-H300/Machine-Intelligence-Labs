from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented

#Done: Import any modules you want to use
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #Done: ADD YOUR CODE HERE
    #My-Comment: check whether the initial state is the Goal
    if problem.is_goal(initial_state):
        return []
    #My-Comment: create a queue to store the states
    frontier = deque()
    frontier.append(initial_state)
    #My-Comment: create a set to store the explored states
    explored = set()
    #My-Comment: dictionary to add the path for each node
    path = {}
    path[initial_state] = []
    #My-Comment: loop until the queue is empty
    while frontier:
        #My-Comment: get the first state from the queue
        #My-Comment: here we want the sibiling so pop left
        node = frontier.popleft()
        #My-Comment: add it to explored nodes
        explored.add(node)
        #My-Comment: get all the actions from the current state
        actions = problem.get_actions(node)
        #My-Comment: loop over all the actions
        for action in actions:
            #My-Comment: get the next state from the current state and the action
            child = problem.get_successor(node, action)
            #My-Comment: check whether the state is not explored and not in the queue
            if child not in explored and child not in path:
                # add the cation to get this node
                path[child] = path[node] + [action]
                #My-Comment: check whether the state is the goal
                if problem.is_goal(child):
                    return path[child]
                #My-Comment: add it to the queue
                frontier.append(child)
                
    return None
    # NotImplemented()

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #Done: ADD YOUR CODE HERE
    #My-Comment: check whether the initial state is the Goal
    if problem.is_goal(initial_state):
        return []
    #My-Comment: create a queue to store the states
    frontier = deque()
    frontier.append(initial_state)
    #My-Comment: create a set to store the explored states
    explored = set()
    #My-Comment: dictionary to add the path for each node
    path = {}
    path[initial_state] = []
    #My-Comment: loop until the queue is empty
    while frontier:
        #My-Comment: get the first state from the queue
        #My-Comment: here we want the children so pop
        node = frontier.pop()
        #My-Comment: check whether the state is the goal
        if problem.is_goal(node):
            return path[node]
        #My-Comment: add it to explored nodes
        explored.add(node)
        #My-Comment: get all the actions from the current state
        actions = problem.get_actions(node)
        #My-Comment: loop over all the actions
        for action in actions:
            #My-Comment: get the next state from the current state and the action
            child = problem.get_successor(node, action)
            #My-Comment: check whether the state is not explored and not in the queue
            if child not in explored and child not in path:
                #My-Comment: add it to the queue
                frontier.append(child)
                # add the cation to get this node
                path[child] = path[node] + [action]

    return None
    # NotImplemented()
    

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #Done: ADD YOUR CODE HERE
    #My-Comment: define class for the node
    class Node:
        def __init__(self, state, cost, order, path):
            self.state = state
            self.cost = cost
            self.order = order
            self.path = path

        #My-Comment: Comparison based on cost and order
        def __gt__(self, other):
            if self.cost > other.cost:
                return True
            if self.cost == other.cost:
                return self.order > other.order
            return False

        def __eq__(self, other):
            return self.state == other.state
    
    #My-Comment: check whether the initial state is the Goal
    if problem.is_goal(initial_state):
        return []
    #My-Comment: create an empty priroty queue
    frontier = []
    #My-Comment: dictionary to add nodes position in priority queue
    node_positions = {}
    #My-Comment: To keep track of the order of the nodes entering the
    order = 0 
    #My-Comment: create a set to store the explored states
    explored = set()
    #My-Comment: create the initial node
    initial_node = Node(initial_state, 0, order, [])
    #My-Comment: add the initial node to the queue
    heapq.heappush(frontier, initial_node)
    #My-Comment: add the initial node to the dictionary
    node_positions[initial_state] = initial_node
    #My-Comment: loop until the queue is empty
    while len(frontier):
        #My-Comment: get the first state from the priority queue
        node=heapq.heappop(frontier)
        #My-Comment: remove it from node_position also
        node_positions.pop(node.state)
        #My-Comment: check whether the state is the goal
        if problem.is_goal(node.state):
            return node.path
        #My-Comment: add it to explored nodes
        explored.add(node.state)
        #My-Comment: get all the actions from the current state
        actions = problem.get_actions(node.state)
        #My-Comment: loop over all the actions
        for action in actions:
            #My-Comment: get the next state from the current state and the action
            child = problem.get_successor(node.state, action)
            #My-Comment: get cost, path and order of child and create the node
            path = node.path + [action]
            cost = node.cost + problem.get_cost(node.state, action)
            child_node = Node(child, cost, order, path)
            order += 1
            #My-Comment: check whether the state is not explored and not in the queue
            if child not in explored and child not in node_positions:
                heapq.heappush(frontier, child_node)
                node_positions[child] = child_node
            #My-Comment: check whether the state is in the frontier
            elif child in node_positions:
                #My-Comment: compare the costs
                existing_node = node_positions[child]
                if child_node < existing_node:
                    node_positions[child].state = child_node.state
                    node_positions[child].cost = child_node.cost
                    node_positions[child].order = child_node.order
                    node_positions[child].path = child_node.path
      
    return None
    # NotImplemented()


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #Done: ADD YOUR CODE HERE
    #My-Comment: define class for the node
    class Node:
        def __init__(self, state, path_cost, cost, order, path):
            self.state = state
            self.path_cost = path_cost
            self.cost = cost
            self.order = order
            self.path = path

        #My-Comment: Comparison based on cost and order
        def __gt__(self, other):
            if self.cost > other.cost:
                return True
            if self.cost == other.cost:
                return self.order > other.order
            return False

        def __eq__(self, other):
            return self.state == other.state
    
    #My-Comment: check whether the initial state is the Goal
    if problem.is_goal(initial_state):
        return []
    #My-Comment: create an empty priroty queue
    frontier = []
    #My-Comment: dictionary to add nodes position in priority queue
    node_positions = {}
    #My-Comment: To keep track of the order of the nodes entering the
    order = 0 
    #My-Comment: create a set to store the explored states
    explored = set()
    #My-Comment: create the initial node
    initial_node = Node(initial_state, 0, 0, order, [])
    #My-Comment: add the initial node to the queue
    heapq.heappush(frontier, initial_node)
    #My-Comment: add the initial node to the dictionary
    node_positions[initial_state] = initial_node
    #My-Comment: loop until the queue is empty
    while len(frontier):
        #My-Comment: get the first state from the priority queue
        node=heapq.heappop(frontier)
        #My-Comment: remove it from node_position also
        node_positions.pop(node.state)
        #My-Comment: check whether the state is the goal
        if problem.is_goal(node.state):
            return node.path
        #My-Comment: add it to explored nodes
        explored.add(node.state)
        #My-Comment: get all the actions from the current state
        actions = problem.get_actions(node.state)
        #My-Comment: loop over all the actions
        for action in actions:
            #My-Comment: get the next state from the current state and the action
            child = problem.get_successor(node.state, action)
            #My-Comment: get cost, path and order of child and create the node
            path = node.path + [action]
            path_cost = node.path_cost + problem.get_cost(node.state, action)
            cost = path_cost + heuristic(problem, child)
            child_node = Node(child, path_cost, cost, order, path)
            order += 1
            #My-Comment: check whether the state is not explored and not in the queue
            if child not in explored and child not in node_positions:
                heapq.heappush(frontier, child_node)
                node_positions[child] = child_node
            #My-Comment: check whether the state is in the frontier
            elif child in node_positions:
                #My-Comment: compare the costs
                existing_node = node_positions[child]
                if child_node < existing_node:
                    node_positions[child].state = child_node.state
                    node_positions[child].path_cost = child_node.path_cost
                    node_positions[child].cost = child_node.cost
                    node_positions[child].order = child_node.order
                    node_positions[child].path = child_node.path
      
    return None
    # NotImplemented()

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #Done: ADD YOUR CODE HERE
    #My-Comment: define class for the node
    class Node:
        def __init__(self, state, cost, order, path):
            self.state = state
            self.cost = cost
            self.order = order
            self.path = path

        #My-Comment: Comparison based on cost and order
        def __gt__(self, other):
            if self.cost > other.cost:
                return True
            if self.cost == other.cost:
                return self.order > other.order
            return False

        def __eq__(self, other):
            return self.state == other.state
    
    #My-Comment: check whether the initial state is the Goal
    if problem.is_goal(initial_state):
        return []
    #My-Comment: create an empty priroty queue
    frontier = []
    #My-Comment: dictionary to add nodes position in priority queue
    node_positions = {}
    #My-Comment: To keep track of the order of the nodes entering the
    order = 0 
    #My-Comment: create a set to store the explored states
    explored = set()
    #My-Comment: create the initial node
    initial_node = Node(initial_state, 0, order, [])
    #My-Comment: add the initial node to the queue
    heapq.heappush(frontier, initial_node)
    #My-Comment: add the initial node to the dictionary
    node_positions[initial_state] = initial_node
    #My-Comment: loop until the queue is empty
    while len(frontier):
        #My-Comment: get the first state from the priority queue
        node=heapq.heappop(frontier)
        #My-Comment: remove it from node_position also
        node_positions.pop(node.state)
        #My-Comment: check whether the state is the goal
        if problem.is_goal(node.state):
            return node.path
        #My-Comment: add it to explored nodes
        explored.add(node.state)
        #My-Comment: get all the actions from the current state
        actions = problem.get_actions(node.state)
        #My-Comment: loop over all the actions
        for action in actions:
            #My-Comment: get the next state from the current state and the action
            child = problem.get_successor(node.state, action)
            #My-Comment: get cost, path and order of child and create the node
            path = node.path + [action]
            cost = heuristic(problem, child)
            child_node = Node(child, cost, order, path)
            order += 1
            #My-Comment: check whether the state is not explored and not in the queue
            if child not in explored and child not in node_positions:
                heapq.heappush(frontier, child_node)
                node_positions[child] = child_node
            #My-Comment: check whether the state is in the frontier
            elif child in node_positions:
                #My-Comment: compare the costs
                existing_node = node_positions[child]
                if child_node < existing_node:
                    node_positions[child].state = child_node.state
                    node_positions[child].cost = child_node.cost
                    node_positions[child].order = child_node.order
                    node_positions[child].path = child_node.path
      
    return None
    # NotImplemented()
    