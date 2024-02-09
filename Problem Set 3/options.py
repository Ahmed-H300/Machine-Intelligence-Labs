# This file contains the options that you should modify to solve Question 2

def question2_1():
    # DONE: Choose options that would lead to the desired results
    # My-Comment: to seek the near terminal state (reward +1) via the short dangerous path
    # My-Comment: living_reward should be big negative
    # My-Comment: environment is stochastic with noise 0.2
    return {
        "noise": 0.2,
        "discount_factor": 0.5,
        "living_reward": -3
    }


def question2_2():
    # DONE: Choose options that would lead to the desired results
    # My-Comment: to seek the near terminal state (reward +1) via the long safe path
    # My-Comment: living_reward should be small negative
    # My-Comment: environment is stochastic with noise 0.2
    # My-Comment: decrease discount factor to make it choose the +1
    return {
        "noise": 0.2,
        "discount_factor": 0.2,
        "living_reward": -0.03
    }


def question2_3():
    # DONE: Choose options that would lead to the desired results
    # My-Comment: to seek the near terminal state (reward +10) via the short path
    # My-Comment: living_reward should be big negative
    # My-Comment: environment is stochastic with noise 0.2
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -2
    }


def question2_4():
    # DONE: Choose options that would lead to the desired results
    # My-Comment: to seek the near terminal state (reward +10) via the long path
    # My-Comment: living_reward should be small negative
    # My-Comment: environment is stochastic with noise 0.2
    return {
        "noise": 0.2,
        "discount_factor": 1,
        "living_reward": -0.1
    }


def question2_5():
    # DONE: Choose options that would lead to the desired results
    # My-Comment: to avoid any terminal state
    # My-Comment: living_reward should be big positive
    return {
        "noise": 0.2,
        "discount_factor": 0.2,
        "living_reward": 20
    }


def question2_6():
    # DONE: Choose options that would lead to the desired results
    # My-Comment: to end in the shortest time possible
    # My-Comment: living_reward should be ver big negative
    return {
        "noise": 0.2,
        "discount_factor": 0.3,
        "living_reward": -30
    }
