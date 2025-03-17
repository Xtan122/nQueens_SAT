from pysat.solvers import Glucose3


def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]


def generate_new_variables(new_variables, new_length):
    last_var = new_variables[-1]
    new_vars = [last_var + i for i in range(1, new_length + 1)]
    new_variables.extend(new_vars)
    return new_variables


def at_most_one(clauses, variables, new_variables):
    if len(variables) <= 1:
        return clauses

    new_length = len(variables) - 1
    start_index = len(new_variables)

    generate_new_variables(new_variables, new_length)

    clauses.append([-variables[0], new_variables[start_index]])

    for i in range(1, new_length):
        clauses.append([-variables[i], new_variables[start_index + i]])
        clauses.append([-new_variables[start_index + i - 1], new_variables[start_index + i]])
        clauses.append([-variables[i], -new_variables[start_index + i - 1]])

    clauses.append([-variables[new_length], -new_variables[start_index + new_length - 1]])

    return clauses


def exactly_one(clauses, variables, new_variables):
    if not variables:
        return clauses

    clauses.append(variables.copy())  # At least one is true
    return at_most_one(clauses, variables, new_variables)  # At most one is true


def generate_clauses(n, variables):
    clauses = []
    new_variables = [n * n]  # Start with n^2 variables

    # Exactly one queen per row
    for i in range(n):
        exactly_one(clauses, variables[i], new_variables)

    # Exactly one queen per column
    for j in range(n):
        exactly_one(clauses, [variables[i][j] for i in range(n)], new_variables)

    # At most one queen per diagonal (top-left to bottom-right)
    for d in range(-n + 1, n):
        diagonal = [variables[i][i + d] for i in range(n) if 0 <= i + d < n]
        if diagonal:
            at_most_one(clauses, diagonal, new_variables)

    # At most one queen per diagonal (top-right to bottom-left)
    for d in range(0, 2 * n - 1):
        diagonal = [variables[i][d - i] for i in range(n) if 0 <= d - i < n]
        if diagonal:
            at_most_one(clauses, diagonal, new_variables)

    return clauses


def solve_n_queens(n):
    variables = generate_variables(n)
    clauses = generate_clauses(n, variables)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        solution = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if model[i * n + j] > 0:
                    solution[i][j] = 1
        return solution
    else:
        return None


def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


n = 4
solution = solve_n_queens(n)
print_solution(solution)