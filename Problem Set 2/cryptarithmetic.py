from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

# DONE (Optional): Import any builtin library or define any helper function you want to use
from itertools import combinations, product

# This is a class to define for cryptarithmetic puzzles as CSPs


class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None:
                continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) + ")"
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match:
            raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        # DONE Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        problem.variables = []
        problem.domains = {}
        problem.constraints = []
        #########################################################
        # My-Comment: get the vairables and add auxilary variables for LSHO and LH1 to be of size of RHS
        LHS0_len = len(LHS0)
        LHS1_len = len(LHS1)
        RHS_len = len(RHS)
        # My-Comment: add the variables of LHS0, LHS1, RHS to the set
        variables_set = set(LHS0 + LHS1 + RHS)
        # My-Comment: add the domains of LHS0, LHS1, RHS to the set
        problem.domains.update({var: set(range(10)) for var in variables_set})
        # My-Comment: add constrain that no vaiable is equal to the other
        problem.constraints.extend([BinaryConstraint([variable, other_variable], lambda x, y: x != y)
                                   for variable, other_variable in combinations(variables_set, 2)])
        # # My-Comment: cast the set to list for the problem variables
        problem.variables = list(variables_set)
        # My-Comment: add carry variable but no carry for first column
        carry_set = [f'C{i}' for i in range(2, RHS_len + 2)]
        problem.variables.extend(carry_set)
        # My-Comment: add the domains of for carry
        problem.domains.update({var: set(range(2)) for var in carry_set})
        # My-Comment: get the left most char in each string and remove 0 from it's domain
        LHS0_left_most_char = LHS0[0]
        LHS1_left_most_char = LHS1[0]
        RHS_left_most_char = RHS[0]
        # My-Comment: add the unary constraints for the left most char in each string
        constraint = UnaryConstraint(LHS0_left_most_char, lambda x: x != 0)
        problem.constraints.append(constraint)
        if LHS1_left_most_char != LHS0_left_most_char:
            constraint = UnaryConstraint(LHS1_left_most_char, lambda x: x != 0)
            problem.constraints.append(constraint)
        if RHS_left_most_char != LHS0_left_most_char and RHS_left_most_char != LHS1_left_most_char:
            constraint = UnaryConstraint(RHS_left_most_char, lambda x: x != 0)
            problem.constraints.append(constraint)
        # My-Comment: generate domain of 2 range(10)
        domain_two = {(i, j) for i, j in product(range(10), repeat=2)}
        # My-Comment:  generate domain of 2 range(2) and range(10)
        domain_two_and_zero = {(i, j) for i, j in product(range(2), range(10))}
        # My-Comment:  generate domain of 2 domain_two_and_zero and range(10)
        domain_three = {(x, y, z) for x, y, z in product(
            set(range(2)), set(range(10)), set(range(10)))}
        # My-Comment: add the binary constraints for the first column
        # My-Comment: define variables
        next_carry_variable = f"C2"
        compined_left = LHS0[-1] + LHS1[-1]
        compined_right = next_carry_variable + RHS[0]
        # My-Comment: extend variables
        problem.variables.extend([compined_left, compined_right])
        problem.domains.update(
            {compined_left: domain_two, compined_right: domain_two_and_zero})
        # My-Comment: define constrains
        constraints = [
            BinaryConstraint([LHS0[-1], compined_left],
                             lambda x, y: x == y[0]),
            BinaryConstraint([LHS1[-1], compined_left],
                             lambda x, y: x == y[1]),
            BinaryConstraint([RHS[-1], compined_right],
                             lambda x, y: x == y[1]),
            BinaryConstraint(
                [next_carry_variable, compined_right], lambda x, y: x == y[0]),
            BinaryConstraint([compined_left, compined_right],
                             lambda x, y: (x[0]+x[1]) == (y[0]*10 + y[1]))
        ]
        # My-Comment: extend constrains
        problem.constraints.extend(constraints)
        # My-Comment: get which is smaller
        smaller_len = min(LHS0_len, LHS1_len)
        # My-Comment: assign domains
        problem.domains.update({compined_left_1: domain_three for compined_left_1 in [
                               f"C{i}" + LHS0[-i] + LHS1[-i] for i in range(2, smaller_len + 1)]})
        problem.domains.update({compined_right: domain_two_and_zero for compined_right in [
                               f"C{i + 1}" + RHS[-i] for i in range(2, smaller_len + 1)]})
        # My-Comment: assign constrains
        problem.constraints.extend(
            [BinaryConstraint([compined_left_1, compined_right], lambda x, y: (x[0]+x[1]+x[2]) == (y[0]*10 + y[1])) for compined_left_1, compined_right in zip(
                [f"C{i}" + LHS0[-i] + LHS1[-i] for i in range(2, smaller_len + 1)], [f"C{i + 1}" + RHS[-i] for i in range(2, smaller_len + 1)])]
        )
        # My-Comment: add the binary constraints for the first smaller_len columns
        # My-Comment: extend variables
        problem.variables.extend(
            [f"C{i}" + LHS0[-i] + LHS1[-i] for i in range(2, smaller_len + 1)])
        problem.variables.extend([f"C{i + 1}" + RHS[-i]
                                 for i in range(2, smaller_len + 1)])
        # My-Comment: define constrains
        constraints = [
            [
                BinaryConstraint(
                    [f"C{i}", f"C{i}" + LHS0[-i] + LHS1[-i]], lambda x, y: x == y[0]),
                BinaryConstraint(
                    [LHS0[-i], f"C{i}" + LHS0[-i] + LHS1[-i]], lambda x, y: x == y[1]),
                BinaryConstraint(
                    [LHS1[-i], f"C{i}" + LHS0[-i] + LHS1[-i]], lambda x, y: x == y[2]),
                BinaryConstraint(
                    [RHS[-i], f"C{i + 1}" + RHS[-i]], lambda x, y: x == y[1]),
                BinaryConstraint(
                    [f"C{i + 1}", f"C{i + 1}" + RHS[-i]], lambda x, y: x == y[0]),
                BinaryConstraint([f"C{i}" + LHS0[-i] + LHS1[-i], f"C{i + 1}" +
                                 RHS[-i]], lambda x, y: (x[0]+x[1]+x[2]) == (y[0]*10 + y[1]))
            ] for i in range(2, smaller_len + 1)
        ]
        # My-Comment: extend constrains
        problem.constraints.extend(
            [constr for sublist in constraints for constr in sublist])
        # My-Comment: get which is bigher
        bigger_len = max(LHS0_len, LHS1_len)
        # My-Comment: get which is the one is bigger
        bigger = LHS0 if LHS0_len > LHS1_len else LHS1
        # My-Comment: assign domains
        problem.domains.update({compined_left: domain_two_and_zero for compined_left in [
                               f"C{i}" + bigger[-i] for i in range(smaller_len + 1, bigger_len + 1)]})
        problem.domains.update({compined_right: domain_two_and_zero for compined_right in [
                               f"C{i + 1}" + RHS[-i] for i in range(smaller_len + 1, bigger_len + 1)]})
        # My-Comment: add the binary constraints for the rest of the columns
        # My-Comment: extend variables
        problem.variables.extend([f"C{i}" + bigger[-i] for i in range(smaller_len + 1, bigger_len + 1)] +
                                 [f"C{i + 1}" + RHS[-i] for i in range(smaller_len + 1, bigger_len + 1)])
        # My-Comment: define constrains
        constraints = [
            [
                BinaryConstraint(
                    [f"C{i}", f"C{i}" + bigger[-i]], lambda x, y: x == y[0]),
                BinaryConstraint(
                    [bigger[-i], f"C{i}" + bigger[-i]], lambda x, y: x == y[1]),
                BinaryConstraint(
                    [RHS[-i], f"C{i + 1}" + RHS[-i]], lambda x, y: x == y[1]),
                BinaryConstraint(
                    [f"C{i + 1}", f"C{i + 1}" + RHS[-i]], lambda x, y: x == y[0]),
                BinaryConstraint([f"C{i}" + bigger[-i], f"C{i + 1}" + RHS[-i]],
                                 lambda x, y: (x[0]+x[1]) == (y[0]*10 + y[1]))
            ] for i in range(smaller_len + 1, bigger_len + 1)
        ]
        # My-Comment: extend constrains
        problem.constraints.extend(
            [constr for sublist in constraints for constr in sublist])
        # My-Comment: add the binary constraints for the rest of the columns
        problem.constraints.extend([BinaryConstraint(
            [RHS[-i], f"C{i}"], lambda x, y: x == y) for i in range(bigger_len + 1, RHS_len + 1)])
        #########################################################

        return problem

    # Read a cryptarithmetic puzzle from a file
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())
