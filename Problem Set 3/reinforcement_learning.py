from typing import Callable, DefaultDict, Dict, Generic, List, Optional, Union
from agents import Agent
from environment import Environment, S, A
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented

import json
from collections import defaultdict

# The base class for all Reinforcement Learning Agents required for this problem set


class RLAgent(Agent[S, A]):
    rng: RandomGenerator  # A random number generator used for exploration
    actions: List[A]  # A list of all actions that the environment accepts
    discount_factor: float  # The discount factor "gamma"
    epsilon: float  # The exploration probability for epsilon-greedy
    learning_rate: float  # The learning rate "alpha"

    def __init__(self,
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__()
        # initialize the random generator with a seed for reproducability
        self.rng = RandomGenerator(seed)
        self.actions = actions
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.learning_rate = learning_rate

    # A virtual function that returns the Q-value for a specific state and action
    # This should be overriden by the derived RL agents
    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        return 0

    # Returns true if we should explore (rather than exploit)
    def should_explore(self) -> bool:
        return self.rng.float() < self.epsilon

    def act(self, env: Environment[S, A], observation: S, training: bool = False) -> A:
        actions = env.actions()
        if training and self.should_explore():
            # DONE: Return a random action whose index is "self.rng.int(0, len(actions)-1)"
            # My-Comment: Generate a random integer between 0 and the length of the actions list minus 1
            # My-Comment: Use this random integer as an index to select a random action from the actions list
            return actions[self.rng.int(0, len(actions)-1)]
            # NotImplemented()
        else:
            # DONE: return the action with the maximum q-value as calculated by "compute_q" above
            # if more than one action has the maximum q-value, return the one that appears first in the "actions" list
            # # My-Comment: Initialize the maximum Q value to negative infinity
            # max_q_value = float('-inf')

            # # My-Comment: Initialize the action that gives the maximum Q value to None
            # max_action = None

            # # My-Comment: Loop over all actions
            # for action in actions:
            #     # My-Comment: Compute the Q value for the current action
            #     q_value = self.compute_q(env, observation, action)

            #     # My-Comment: If the Q value for the current action is greater than the maximum Q value
            #     if q_value > max_q_value:
            #         # My-Comment: Update the maximum Q value
            #         max_q_value = q_value
            #         # My-Comment: Update the action that gives the maximum Q value
            #         max_action = action
            max_action = max(actions, key=lambda action: self.compute_q(env, observation, action), default=None)
            return max_action
            # NotImplemented()

#############################
#######     SARSA      ######
#############################

# This is a class for a generic SARSA agent


class SARSALearningAgent(RLAgent[S, A]):
    Q: DefaultDict[S, DefaultDict[A, float]]  # The table of the Q values
    # The first key is the string representation of the state
    # The second key is the string representation of the action
    # The value is the Q-value of the given state and action

    def __init__(self,
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        self.Q = defaultdict(lambda: defaultdict(
            lambda: 0))  # The default Q value is 0

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        # Return the Q-value of the given state and action
        return self.Q[state][action]
        # NOTE: we cast the state and the action to a string before querying the dictionaries

    # Update the value of Q(state, action) using this transition via the SARSA update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, next_action: Optional[A]):
        # DONE: Complete this function to update Q-table using the SARSA update rule
        # If next_action is None, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
        # My-Comment: Q(s, a) = Q(s, a) + alpha * (r + gamma * Q(s', a') - Q(s, a))
        # My-Comment: Check if the next action is None
        if next_action is None:
            # My-Comment: If it is, set the next Q value to 0
            next_q_value = 0
        else:
            # My-Comment: If it's not, compute the next Q value using the next state and action
            next_q_value = self.compute_q(env, next_state, next_action)

        # My-Comment: Compute the current Q value using the current state and action
        current_q_value = self.compute_q(env, state, action)

        # My-Comment: Compute the new Q value using the formula for Q-learning
        new_q_value = current_q_value + self.learning_rate * (reward + self.discount_factor * next_q_value - current_q_value)

        # My-Comment: Update the Q value for the current state and action in the Q table
        self.Q[state][action] = new_q_value
        # NotImplemented()

    # Save the Q-table to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            Q = {
                env.format_state(state): {
                    env.format_action(action): value for action, value in state_q.items()
                } for state, state_q in self.Q.items()
            }
            json.dump(Q, f, indent=2, sort_keys=True)

    # load the Q-table from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            Q = json.load(f)
            self.Q = {
                env.parse_state(state): {
                    env.parse_action(action): value for action, value in state_q.items()
                } for state, state_q in Q.items()
            }

#############################
#####   Q-Learning     ######
#############################

# This is a class for a generic Q-learning agent


class QLearningAgent(RLAgent[S, A]):
    Q: DefaultDict[str, DefaultDict[str, float]]  # The table of the Q values
    # The first key is the string representation of the state
    # The second key is the string representation of the action
    # The value is the Q-value of the given state and action

    def __init__(self,
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        self.Q = defaultdict(lambda: defaultdict(
            lambda: 0))  # The default Q value is 0

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        # Return the Q-value of the given state and action
        return self.Q[state][action]
        # NOTE: we cast the state and the action to a string before querying the dictionaries

    # Given a state, compute and return the utility of the state using the function "compute_q"
    def compute_utility(self, env: Environment[S, A], state: S) -> float:
        # DONE: Complete this function.
        # My-Comment: Compute the maximum Q value for the current state by taking the maximum over all Q values in the Q table for the current state
        max_q_value = max([self.compute_q(env, state, action) for action in env.actions()])

        # My-Comment: Return the maximum Q value
        return max_q_value
        # NotImplemented()

    # Update the value of Q(state, action) using this transition via the Q-Learning update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, done: bool):
        # DONE: Complete this function to update Q-table using the Q-Learning update rule
        # If done is True, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
        # My-Comment: Check if the episode is done (i.e., if we're in a terminal state)
        # My-Comment: Q(s, a) = Q(s, a) + alpha * (r + gamma * max(Q(s', a')) - Q(s, a))
        # My-Comment: Compute the current Q value for the given state and action
        current_q_value = self.Q[state][action]

        # My-Comment: Compute the utility of the next state
        next_state_utility = self.compute_utility(env, next_state)

        # My-Comment: Multiply the utility of the next state by the discount factor
        discounted_next_state_utility = self.discount_factor * next_state_utility

        # My-Comment: Add the reward to the discounted utility of the next state
        reward_plus_discounted_utility = reward + discounted_next_state_utility

        # My-Comment: Subtract the current Q value from the result of the previous step
        delta = reward_plus_discounted_utility - current_q_value

        # My-Comment: Multiply the result of the previous step by the learning rate
        learning_rate_delta = self.learning_rate * delta

        # My-Comment: Add the result of the previous step to the current Q value to get the new Q value
        new_q_value = current_q_value + learning_rate_delta

        # My-Comment: Update the Q value for the given state and action in the Q table with the new Q value
        self.Q[state][action] = new_q_value
        # NotImplemented()

    # Save the Q-table to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            Q = {
                env.format_state(state): {
                    env.format_action(action): value for action, value in state_q.items()
                } for state, state_q in self.Q.items()
            }
            json.dump(Q, f, indent=2, sort_keys=True)

    # load the Q-table from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            Q = json.load(f)
            self.Q = {
                env.parse_state(state): {
                    env.parse_action(action): value for action, value in state_q.items()
                } for state, state_q in Q.items()
            }

#########################################
#####   Approximate Q-Learning     ######
#########################################
# The type definition for a set of features representing a state
# The key is the feature name and the value is the feature value
Features = Dict[str, float]

# This class takes a state and returns the a set of features


class FeatureExtractor(Generic[S, A]):

    # Returns a list of feature names.
    # This will be used by the Approximate Q-Learning agent to initialize its weights dictionary.
    @property
    def feature_names(self) -> List[str]:
        return []

    # Given an enviroment and an observation (a state), return a set of features that represent the given state
    def extract_features(self, env: Environment[S, A], state: S) -> Features:
        return {}

# This is a class for a generic Q-learning agent


class ApproximateQLearningAgent(RLAgent[S, A]):
    weights: Dict[A, Features]    # The weights dictionary for this agent.
    # The first key is action and the second key is the feature name
    # The value is the weight
    # The feature extractor used to extract the features corresponding to a state
    feature_extractor: FeatureExtractor[S, A]

    def __init__(self,
                 feature_extractor: FeatureExtractor[S, A],
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        feature_names = feature_extractor.feature_names
        self.weights = {action: {feature: 0 for feature in feature_names}
                        for action in actions}  # we initialize the weights to 0
        self.feature_extractor = feature_extractor

    # Given the features of state and an action, compute and return the Q value
    def __compute_q_from_features(self, features: Dict[str, float], action: A) -> float:
        # DONE: Complete this function
        # NOTE: Remember to cast the action to string before quering self.weights
        # My-Comment: Q(s, a) = sum(w_i * f_i)
        # My-Comment: Compute the Q value by summing the product of each feature value and its corresponding weight
        return sum(features[feature] * self.weights[action][feature] for feature in features)
        # NotImplemented()

    # Given the features of a state, compute and return the utility of the state using the function "__compute_q_from_features"
    def __compute_utility_from_features(self, features: Dict[str, float]) -> float:
        # DONE: Complete this function
        # My-Comment: Compute the utility by finding the maximum Q value over all actions, computed from the features
        utility = max([self.__compute_q_from_features(features, action) for action in self.actions])

        # My-Comment: Return the computed utility
        return utility
        # NotImplemented()

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        features = self.feature_extractor.extract_features(env, state)
        return self.__compute_q_from_features(features, action)

    # Update the value of Q(state, action) using this transition via the Q-Learning update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, done: bool):
        # DONE: Complete this function to update weights using the Q-Learning update rule
        # If done is True, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0

        # My-Comment: check if next state is terminal state
        if done:
            # My-Comment: if it is, set the next Q value to 0
            next_q_value = 0
        else:
            # My-Comment: if it's not, extract the features from the next state
            next_features = self.feature_extractor.extract_features(env, next_state)
            # My-Comment: compute the Q value for the next state using the features
            next_q_value = self.__compute_utility_from_features(next_features)
        # My-Comment: Compute the current Q value for the current state and action
        current_q_value = self.compute_q(env, state, action)
        # My-Comment: Copy of weights
        weights_temp = self.weights.copy()
        # My-Comment: Extract the features from the current state
        features = self.feature_extractor.extract_features(env, state)
        # My-Comment: update the weights by the following rule
        # My-Comment: w_i = w_i + alpha * (r + gamma * max(Q(s', a')) - Q(s, a)) * f_i
        # My-Comment: where w_i is the weight of the feature f_i
        # My-Comment: alpha is the learning rate
        # My-Comment: r is the reward
        # My-Comment: gamma is the discount factor
        # My-Comment: Compute the error
        error = reward + self.discount_factor * next_q_value - current_q_value
        # My-Comment: Update the weights
        for feature in features:
            weights_temp[action][feature] = self.weights[action][feature] + self.learning_rate * error * features[feature]

        # My-Comment: update the weights
        self.weights = weights_temp
        # NotImplemented()

    # Save the weights to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            weights = {env.format_action(
                action): w for action, w in self.weights.items()}
            json.dump(weights, f, indent=2, sort_keys=True)

    # load the weights from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            weights = json.load(f)
            self.weights = {env.parse_action(
                action): w for action, w in weights.items()}
