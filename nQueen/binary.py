from pysat.solvers import Glucose3
import math

def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

def binary_encoding(clauses, target, new_variables):
    for i in range(len(new_variables)):
        clauses.append([-target, new_variables[i]])

def generate_binary_combinations(n):
    binary_combinations = []
    for i in range(1 << n):
        binary_combinations.append(format(i, '0' + str(n) + 'b'))
    return binary_combinations

def generate_new_variables(end, length):
    num_new_vars = max(1, math.ceil(math.log(length + 1, 2)))
    return [i for i in range(end + 1, end + num_new_vars + 1)]

def at_most_one(clauses, new_variables, variables):
    if len(variables) <= 1:
        return

    temp_new_variables = generate_new_variables(n ** 2 + len(new_variables), len(variables))
    new_variables += temp_new_variables
    binary_combinations = generate_binary_combinations(len(temp_new_variables))

    for i in range(min(len(variables), len(binary_combinations))):
        combination = binary_combinations[i]
        temp_clause = []

        for bit_position in range(len(combination) - 1, -1, -1):
            index = len(combination) - bit_position - 1
            if index < len(temp_new_variables):
                bit_value = int(combination[bit_position])

                if bit_value == 1:
                    temp_clause.append(temp_new_variables[index])
                else:
                    temp_clause.append(-temp_new_variables[index])

        binary_encoding(clauses, variables[i], temp_clause)

def exactly_one(clauses, new_variables, variables):
    clauses.append(variables)
    at_most_one(clauses, new_variables, variables)

def generate_clauses(n, variables):
    clauses = []
    new_variables = []

    for i in range(n):
        exactly_one(clauses, new_variables, variables[i])

    for j in range(n):
        exactly_one(clauses, new_variables, [variables[i][j] for i in range(n)])

    for d in range(-n + 1, n):
        diagonal = [variables[i][j] for i in range(n) for j in range(n) if (i - j) == d]
        at_most_one(clauses, new_variables, diagonal)

    for d in range(0, 2 * n - 1):
        diagonal = [variables[i][j] for i in range(n) for j in range(n) if (i + j) == d]
        at_most_one(clauses, new_variables, diagonal)

    return clauses

def solve_n_queens(n):
    variables = generate_variables(n)
    clauses = generate_clauses(n, variables)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        return [[int(model[i * n + j] > 0) for j in range(n)] for i in range(n)]
    else:
        return None

def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))

# Chạy thử nghiệm
n = 512
solution = solve_n_queens(n)
print_solution(solution)
