from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent


class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A]  # The MDP used by this agent for training
    utilities: Dict[S, float]  # The computed utilities
    # The key is the string representation of the state and the value is the utility
    discount_factor: float  # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        # We initialize all the utilities to be 0
        self.utilities = {state: 0 for state in self.mdp.get_states()}
        self.discount_factor = discount_factor

    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        # DONE: Complete this function
        # My-Comment: Check if it is terminal state then return 0
        if self.mdp.is_terminal(state): return 0
        # # My-Comment: Initialize the maximum utility to negative infinity
        # max_utility = float('-inf')

        # # My-Comment: Loop over all actions for the current state
        # for action in self.mdp.get_actions(state):
        #     # My-Comment: Initialize the utility for the current action to 0
        #     action_utility = 0

        #     # My-Comment: Loop over all successor states for the current state and action
        #     for next_state in self.mdp.get_successor(state, action):
        #         # My-Comment: Add the product of the probability and the sum of the reward and the discounted utility of the next state to the utility of the current action
        #         action_utility += self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state])

        #     # My-Comment: Update the maximum utility if the utility of the current action is greater
        #     max_utility = max(max_utility, action_utility)

        # # My-Comment: Return the maximum utility
        # return max_utility
        # My-Comment: Return the maximum utility with list comprehension
        utility = max([sum([self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor *
                      self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action)]) for action in self.mdp.get_actions(state)])
        return utility
        # NotImplemented()

    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        # DONE: Complete this function

        # # My-Comment: Create a new dictionary to store the new utilities
        # new_utilities = {}

        # # My-Comment: Loop over all states
        # for state in self.mdp.get_states():
        #     # My-Comment: Compute the Bellman value for the current state and store it in the new utilities dictionary
        #     new_utilities[state] = self.compute_bellman(state)

        # # My-Comment: Initialize the maximum utility change to 0
        # max_utility_change = 0

        # # My-Comment: Loop over all states
        # for state in self.mdp.get_states():
        #     # My-Comment: Compute the absolute difference between the new and old utility for the current state
        #     utility_change = abs(new_utilities[state] - self.utilities[state])
        #     # My-Comment: Update the maximum utility change if the current utility change is greater
        #     max_utility_change = max(max_utility_change, utility_change)

        # # My-Comment: Update the utilities with the new utilities
        # self.utilities = new_utilities

        # # My-Comment: Check if the maximum utility change is less than or equal to the tolerance and return the result
        # return max_utility_change <= tolerance

        # My-Comment: Compute the bellman equation for each state and update the utility
        # My-Comment: Check if the maximum utility change is less or equal the tolerance
        # My-Comment: Return True if the utilities has converged and False otherwise
        new_utilities = {state: self.compute_bellman(
            state) for state in self.mdp.get_states()}
        max_utility_change = max(abs(
            new_utilities[state] - self.utilities[state]) for state in self.mdp.get_states())
        self.utilities = new_utilities
        return max_utility_change <= tolerance
        # NotImplemented()

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        # DONE: Complete this function to apply value iteration for the given number of iterations
        # My-Comment: Check if the number of iterations is None, then update until the utilities has converged
        # My-Comment: Otherwise, update for the given number of iterations
        # My-Comment: Return the number of iterations that have been run
        iteration_num = 0
        while iterations is None or iteration_num < iterations:
            iteration_num += 1
            if self.update(tolerance):
                break
        # My-Comment: with list comprehension
        # My-Comment: Return the number of iterations that have been run
        # iteration_num = next((i for i in range(1, iterations + 1) if self.update(tolerance) or i == iterations), 0)
        return iteration_num
        # NotImplemented()

    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        # DONE: Complete this function
        # My-Comment: Check if the state is terminal, return None
        if self.mdp.is_terminal(state): return None

        # # My-Comment: Initialize the maximum utility to negative infinity
        # max_utility = float('-inf')

        # # My-Comment: Initialize the best action to None
        # best_action = None

        # # My-Comment: Loop over all actions for the current state
        # for action in self.mdp.get_actions(state):
        #     # My-Comment: Initialize the utility for the current action to 0
        #     action_utility = 0

        #     # My-Comment: Loop over all successor states for the current state and action
        #     for next_state in self.mdp.get_successor(state, action):
        #         # My-Comment: Add the product of the probability and the sum of the reward and the discounted utility of the next state to the utility of the current action
        #         action_utility += self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state])

        #     # My-Comment: If the utility of the current action is greater than the maximum utility, update the maximum utility and the best action
        #     if action_utility > max_utility:
        #         max_utility = action_utility
        #         best_action = action

        # My-Comment: with list comprehension
        # My-Comment: Get the list of all possible actions for the current state
        # My-Comment: For each action, calculate the sum of the product of the probability of reaching the next state and the sum of the reward for the action and the discounted utility of the next state
        # My-Comment: Choose the action that maximizes this sum
        best_action =  max(self.mdp.get_actions(state), key=lambda action: sum([self.mdp.get_successor(state, action)[next_state] * (self.mdp.get_reward(state, action, next_state) + self.discount_factor * self.utilities[next_state]) for next_state in self.mdp.get_successor(state, action)]))

        # My-Comment: Return the chosen action
        return best_action
        # NotImplemented()

    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(
                state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)

    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(
                state): value for state, value in utilities.items()}
