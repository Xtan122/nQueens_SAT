from pysat.solvers import Glucose3

def generate_variables(n):
    return [[i * n + j + 1 for j in range(n)] for i in range(n)]

def generate_new_variables(n, k, last_in_variables):
    return [[last_in_variables + i * k + j + 1 for j in range(k)] for i in range(n - 1)]

def at_least_k(clauses, variables, k):
    n = len(variables)
    last_in_variables = variables[-1][-1]
    new_variables = generate_new_variables(n, k, last_in_variables)

    # (1): Xi -> Ri,1
    for i in range(n - 1):
        clauses.append([-variables[i], new_variables[i][0]])

    # (2): R(i-1),j -> Ri,j
    for i in range(1, n - 1):
        for j in range(0, min(i, k)):
            clauses.append([-new_variables[i-1][j], new_variables[i][j]])

    # (3): Xi and R(i-1),(j-1) -> Ri,j
    for i in range(1, n - 1):
        for j in range(1, min(i + 1, k)):
            clauses.append([-variables[i], -new_variables[i - 1][j - 1], new_variables[i][j]])

    # (4): not_Xi and not_R(i-1),j -> not_Ri,j
    for i in range(1, n - 1):
        for j in range(0, min(i, k)):
            clauses.append([variables[i], new_variables[i-1][j], -new_variables[i][j]])

    # (5): not_Xi -> not_Ri,i
    for i in range(k):
        clauses.append([variables[i], -new_variables[i][i]])

    # (6): not_R(i-1),(j-1) -> not_Ri,j
    for i in range(1, len(variables) - 1):
        for j in range(1, min(i + 1, k)):
            clauses.append([new_variables[i - 1][j - 1], -new_variables[i][j]])

    # (7): R(n-1),k or (Xn and R(n-1)(k-1))
    clauses.append([new_variables[n - 2][k - 1], variables[n - 1]])
    if k - 2 >= 0:
        clauses.append([new_variables[n - 2][k - 1], new_variables[n - 2][k - 2]])

    return clauses

def at_most_k(clauses, variables, k, last_in_variables):
    n = len(variables)
    new_variables = generate_new_variables(n, k, last_in_variables)

    # (1): Xi -> Ri,1
    for i in range(n - 1):
        clauses.append([-variables[i], new_variables[i][0]])

    # (2): R(i-1),j -> Ri,j
    for i in range(1, n - 1):
        for j in range(min(i, k)):
            clauses.append([-new_variables[i - 1][j], new_variables[i][j]])

    # (3): Xi and R(i-1),(j-1) -> Ri,j
    for i in range(1, n - 1):
        for j in range(1, min(i + 1, k)):
            clauses.append([-variables[i], -new_variables[i - 1][j - 1], new_variables[i][j]])

    # (8): Xi -> not_R(i-1),k
    for i in range(k, len(variables)):
        clauses.append([-variables[i], -new_variables[i - 1][k - 1]])

    return clauses

def exactly_k(clauses, variables, k):
    clauses = at_least_k(clauses, variables, k)
    clauses = at_most_k(clauses, variables, k)

    return clauses

def exactly_one(clauses, variables):
    clauses = exactly_k(clauses, variables, 1)

    return clauses

def generate_clauses(n, variables, last_in_variables):
    clauses = []

    # Exactly one queen per row
    for i in range(n):
        exactly_one(clauses, variables[i])

    # Exactly one queen per column
    for j in range(n):
        exactly_one(clauses, [variables[i][j] for i in range(n)])
    # At most one queen per diagonal (top-left to bottom-right)
    for d in range(-n + 1, n):
        diagonal = [variables[i][i + d] for i in range(n) if 0 <= i + d < n]
        if diagonal:
            at_most_k(clauses, diagonal, 1)

    # At most one queen per diagonal (top-right to bottom-left)
    for d in range(0, 2 * n - 1):
        diagonal = [variables[i][d - i] for i in range(n) if 0 <= d - i < n]
        if diagonal:
            at_most_k(clauses, diagonal, 1)

    return clauses

def solve_N_queens(N):
    variables = generate_variables(N)
    last_in_variables = variables[-1][-1]

    clauses = generate_clauses(N, variables, last_in_variables)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        return [[int(model[i * N + j] > 0) for j in range(N)] for i in range(N)]
    else:
        return None


def print_solution(solution):
    if solution is None:
        print("No solution found.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


N = 16
solution = solve_N_queens(N)
print_solution(solution)