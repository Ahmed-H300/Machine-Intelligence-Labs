from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #DONE: Write this function
    # My-Comment: get the constrains of the problem
    constraints = problem.constraints
    # My-Comment: I will loop over the constraints
    for constraint in constraints:
        # My-Comment: Check whether it is binary constrain or not
        # My-Comment: Check whether if it is related to the assigned_variable
        if isinstance(constraint, BinaryConstraint) and assigned_variable in constraint.variables:
            # My-Comment: get the other variable
            other_variable = constraint.get_other(assigned_variable)
            # My-Comment: check if it is assigned skip
            if other_variable not in domains:
                continue
            # My-Comment: calculate the new domain
            new_domain = {value for value in domains[other_variable] if constraint.is_satisfied({assigned_variable: assigned_value, other_variable: value})}
            # My-Comment: if it is empty return false
            if len(new_domain) == 0:
                return False
            # My-Comment: assign the new domain
            domains[other_variable] = new_domain
    # My-Comment: Return True if nothing is empty
    return True
    # NotImplemented()

# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #DONE: Write this function
    # My-Comment: initialize conflict values
    conflict_values = {}
    # My-Comment: get the domain of the variable
    domain = domains[variable_to_assign]
    # My-Comment: set conflict_values to 0
    conflict_values = {value: 0 for value in domain}
    # My-Comment: loop over the domain
    for value in domain:
        # My-Comment: loop over the constraints
        for constraint in problem.constraints:
            # My-Comment: Check whether it is binary constrain or not
            # My-Comment: Check whether if it is related to the assigned_variable
            if isinstance(constraint, BinaryConstraint) and variable_to_assign in constraint.variables:
                # My-Comment: get the other variable
                other_variable = constraint.get_other(variable_to_assign)
                # My-Comment: check if it is assigned skip
                if other_variable not in domains:
                    continue
                # My-Comment: calculate count of unsatisfied constrains
                # My-Comment: get the domain of the other value
                domain_other_value = domains[other_variable]
                conflict_values[value] += sum(1 for other_value in domain_other_value if not constraint.is_satisfied({variable_to_assign: value, other_variable: other_value}))

    # My-Comment: sort then return the list
    return sorted(conflict_values, key=lambda x: (conflict_values[x], x))
    # NotImplemented()

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    #DONE: Write this function
    # My-Comment: check the one consistency to return none if not 1-Consistency
    if not one_consistency(problem):
        return None
    # My-Comment: set the assignment variable
    assignment = {}
    # My-Comment: define the backTrack Algo
    def backTrack(problem: Problem, assignment: Assignment, domains: Dict[str, set]):
        # My-Comment: check if the assignment is complete
        if problem.is_complete(assignment):
            return assignment
        # My-Comment: get the variable to assign
        variable_to_assign = minimum_remaining_values(problem, domains)
        # My-Comment: get the values of the variable
        values = least_restraining_values(problem, variable_to_assign, domains)
        # My-Comment: loop over the values
        for value in values:
            # My-Comment: make the assignment copy
            assignment_copy = assignment.copy()
            # My-Comment: assign the value
            assignment_copy[variable_to_assign] = value
            # My-Comment: make the domain copy
            domains_copy = domains.copy()
            # My-Comment: remove the variable from the domain
            domains_copy.pop(variable_to_assign)
            # My-Comment: check if the value is consistent
            if forward_checking(problem, variable_to_assign, value, domains_copy):
                # My-Comment: get the result
                result = backTrack(problem, assignment_copy, domains_copy)
                # My-Comment: check if the result is not none
                if result is not None:
                    return result
        # My-Comment: return None if no solution found
        return None
    
    # My-Comment: return the result
    return backTrack(problem, assignment, problem.domains)
    # NotImplemented()
    