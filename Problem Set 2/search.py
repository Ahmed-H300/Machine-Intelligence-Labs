from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#DONE: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #DONE: Complete this function
    # My-Comment: get the player
    player_agent = game.get_turn(state)

    # My-Comment: next turn function
    def current_turn(state: S, max_depth: int) -> Tuple[float, A]:
        # My-Comment: check for terminal state
        terminal, values = game.is_terminal(state)
        # My-Comment: if terminal return state utility
        if terminal: return values[player_agent], None
        # My-Comment: if max depth reached return heuristic value
        if max_depth == 0: return heuristic(game, state, player_agent), None
        # My-Comment: get the current agent
        current_agent = game.get_turn(state)
        # My-Comment: check if 0 then max agent
        if current_agent == 0:
            return max_value(state, max_depth)
        else:
            return min_value(state, max_depth)
        
    # My-Comment: max value function
    def max_value(state: S, max_depth: int) -> Tuple[float, A]:
        # My-Comment: get the max value and action
        v, a = float('-inf'), None
        # My-Comment: get actions
        actions = game.get_actions(state)
        # My-Comment: loop over actions
        for action in actions:
            # My-Comment: get successor
            successor = game.get_successor(state, action)
            # My-Comment: get the value of the successor
            value, _ = current_turn(successor, max_depth - 1)
            # My-Comment: compare to get the max
            if value > v:
                v, a = value, action
        return v, a
    
    # My-Comment: min value function
    def min_value(state: S, max_depth: int) -> Tuple[float, A]:
        # My-Comment: get the min value and action
        v, a = float('inf'), None
        # My-Comment: get actions
        actions = game.get_actions(state)
        # My-Comment: loop over actions
        for action in actions:
            # My-Comment: get successor
            successor = game.get_successor(state, action)
            # My-Comment: compare to get the min
            value, _ = current_turn(successor, max_depth - 1)
            if value < v:
                v, a = value, action
        return v, a
    
    # My-Comment: Call the recursive function with initial parameters
    return current_turn(state, max_depth)
    # NotImplemented()

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #DONE: Complete this function
    # My-Comment: get the player
    player_agent = game.get_turn(state)

    # My-Comment: next turn function
    def current_turn(state: S, max_depth: int, alpha: float, beta: float) -> Tuple[float, A]:
        # My-Comment: check for terminal state
        terminal, values = game.is_terminal(state)
        # My-Comment: if terminal return state utility
        if terminal: return values[player_agent], None
        # My-Comment: if max depth reached return heuristic value
        if max_depth == 0: return heuristic(game, state, player_agent), None
        # My-Comment: get the current agent
        current_agent = game.get_turn(state)
        # My-Comment: check if 0 then max agent
        if current_agent == 0:
            return max_value(state, max_depth, alpha, beta)
        else:
            return min_value(state, max_depth, alpha, beta)
        
    # My-Comment: max value function
    def max_value(state: S, max_depth: int, alpha: float, beta: float) -> Tuple[float, A]:
        # My-Comment: get the max value and action
        v, a = float('-inf'), None
        # My-Comment: get actions
        actions = game.get_actions(state)
        # My-Comment: for loop on actions to get successors
        for action in actions:
            # My-Comment: get successor
            successor = game.get_successor(state, action)
            # My-Comment: get the value of the successor
            value, _ = current_turn(successor, max_depth - 1, alpha, beta)
            # My-Comment: compare to get the max
            if value > v:
                v, a = value, action
            # My-Comment: if the maximum value is greater than or equal to the beta
            # My-Comment: return the maximum as no need for further search
            # My-Comment: as beta is the maximum value that minimizer make
            # My-Comment: The minimizing player already has a move that is as good as or better than what they would get from this branch.
            if v >= beta: return v, a
            # My-Comment: update alpha with the max value
            # My-Comment: to make the alpha the best value that the maximizer can gurantee
            alpha = max(alpha, v)
        return v, a

    
    # My-Comment: min value function
    def min_value(state: S, max_depth: int, alpha: float, beta: float) -> Tuple[float, A]:
        # My-Comment: get the min value and action
        v, a = float('inf'), None
        # My-Comment: get actions
        actions = game.get_actions(state)
        # My-Comment: for loop on actions to get successors
        for action in actions:
            # My-Comment: get successor
            successor = game.get_successor(state, action)
            # My-Comment: get the value of the successor
            value, _ = current_turn(successor, max_depth - 1, alpha, beta)
            # My-Comment: compare to get the min
            if value <= v:
                v, a = value, action
            # My-Comment: if the minimum value is less than or equal to the alpha
            # My-Comment: return the minimum as no need for further search
            # My-Comment: as alpha is the minimum value that maximizer make
            # My-Comment: The maximizing player already has a move that is as good as or better than what they would get from this branch.
            if v <= alpha: return v, a
            # My-Comment: update beta with the min value
            # My-Comment: to make the beta the best value that the minimizer can gurantee
            beta = min(beta, v)
        return v, a
 
    # My-Comment: Call the recursive function with initial parameters
    return current_turn(state, max_depth, float('-inf'), float('inf'))
    # NotImplemented()

# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #DONE: Complete this function
    # My-Comment: get the player
    player_agent = game.get_turn(state)

    # My-Comment: next turn function
    def current_turn(state: S, max_depth: int, alpha: float, beta: float) -> Tuple[float, A]:
        # My-Comment: check for terminal state
        terminal, values = game.is_terminal(state)
        # My-Comment: if terminal return state utility
        if terminal: return values[player_agent], None
        # My-Comment: if max depth reached return heuristic value
        if max_depth == 0: return heuristic(game, state, player_agent), None
        # My-Comment: get the current agent
        current_agent = game.get_turn(state)
        # My-Comment: check if 0 then max agent
        if current_agent == 0:
            return max_value(state, max_depth, alpha, beta)
        else:
            return min_value(state, max_depth, alpha, beta)
        
    # My-Comment: max value function
    def max_value(state: S, max_depth: int, alpha: float, beta: float) -> Tuple[float, A]:
        # My-Comment: get the max value and action
        v, a = float('-inf'), None
        # My-Comment: iterate over all possible actions and get action and successor
        actions_successor_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        # My-Comment: sort the actions based on the heuristic value value in descending
        actions_successor_states.sort(key=lambda x: heuristic(game, x[1], player_agent), reverse=True)
        # My-Comment: for loop on actions to get successors
        for action, successor in actions_successor_states:
            # My-Comment: get the value of the successor
            value, _ = current_turn(successor, max_depth - 1, alpha, beta)
            # My-Comment: compare to get the max
            if value > v:
                v, a = value, action
            # My-Comment: if the maximum value is greater than or equal to the beta
            # My-Comment: return the maximum as no need for further search
            # My-Comment: as beta is the maximum value that minimizer make
            # My-Comment: The minimizing player already has a move that is as good as or better than what they would get from this branch.
            if v >= beta: return v, a
            # My-Comment: update alpha with the max value
            # My-Comment: to make the alpha the best value that the maximizer can gurantee
            alpha = max(alpha, v)
        return v, a

    
    # My-Comment: min value function
    def min_value(state: S, max_depth: int, alpha: float, beta: float) -> Tuple[float, A]:
        # My-Comment: get the min value and action
        v, a = float('inf'), None
        # My-Comment: iterate over all possible actions and get action and successor
        actions_successor_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
        # My-Comment: sort the actions based on the heuristic value value in ascending
        actions_successor_states.sort(key=lambda x: heuristic(game, x[1], player_agent))
        # My-Comment: for loop on actions to get successors
        for action, successor in actions_successor_states:
            # My-Comment: get the value of the successor
            value, _ = current_turn(successor, max_depth - 1, alpha, beta)
            # My-Comment: compare to get the min
            if value <= v:
                v, a = value, action
            # My-Comment: if the minimum value is less than or equal to the alpha
            # My-Comment: return the minimum as no need for further search
            # My-Comment: as alpha is the minimum value that maximizer make
            # My-Comment: The maximizing player already has a move that is as good as or better than what they would get from this branch.
            if v <= alpha: return v, a
            # My-Comment: update beta with the min value
            # My-Comment: to make the beta the best value that the minimizer can gurantee
            beta = min(beta, v)
        return v, a
 
    # My-Comment: Call the recursive function with initial parameters
    return current_turn(state, max_depth, float('-inf'), float('inf'))
    # NotImplemented()

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #DONE: Complete this function
    # My-Comment: get the player
    player_agent = game.get_turn(state)

    # My-Comment: next turn function
    def current_turn(state: S, max_depth: int) -> Tuple[float, A]:
        # My-Comment: check for terminal state
        terminal, values = game.is_terminal(state)
        # My-Comment: if terminal return state utility
        if terminal: return values[player_agent], None
        # My-Comment: if max depth reached return heuristic value
        if max_depth == 0: return heuristic(game, state, player_agent), None
        # My-Comment: get the current agent
        current_agent = game.get_turn(state)
        # My-Comment: check if 0 then max agent
        if current_agent == 0:
            return max_value(state, max_depth)
        else:
            return expect_value(state, max_depth)
        
    # My-Comment: max value function
    def max_value(state: S, max_depth: int) -> Tuple[float, A]:
        # My-Comment: get the max value and action
        v, a = float('-inf'), None
        # My-Comment: get actions
        actions = game.get_actions(state)
        # My-Comment: loop over actions
        for action in actions:
            # My-Comment: get successor
            successor = game.get_successor(state, action)
            # My-Comment: get the value of the successor
            value, _ = current_turn(successor, max_depth - 1)
            # My-Comment: compare to get the max
            if value > v:
                v, a = value, action
        return v, a

    
    # My-Comment: min value function
    def expect_value(state: S, max_depth: int) -> Tuple[float, A]:
        # My-Comment: initialize expected value
        expected_value = 0
        # My-Comment: get actions
        actions = game.get_actions(state)
        # My-Comment: for loop on actions to get successors
        for action in actions:
            # My-Comment: get successor
            successor = game.get_successor(state, action)
            # My-Comment: get the value of the successor
            value, _ = current_turn(successor, max_depth - 1)
            # My-Comment: add the value to the expected value
            expected_value += value
        # My-Comment: return the expected value
        return expected_value / len(actions), None
 
    # My-Comment: Call the recursive function with initial parameters
    return current_turn(state, max_depth)
    # NotImplemented()