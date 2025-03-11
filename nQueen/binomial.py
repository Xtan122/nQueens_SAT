from pysat.solvers import Glucose3

def var(i, j , N):
    return i * N + j + 1

def at_least_one(solver, variables):
    solver.add_clause(variables)

def at_most_one(solver, variables):
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            solver.add_clause([-variables[i], -variables[j]])

def exactly_one(solver, variables):
    at_least_one(solver, variables)
    at_most_one(solver, variables)

# Ràng buộc 1: Mỗi hàng chính xác một quân hậu
def only_one_queen_on_row(solver, N):
    for i in range(N):
        exactly_one(solver, [var(i, j, N) for j in range(N)])

# Ràng buộc 2: Mỗi cột chính xác một quân hậu <=> Mỗi cột tối đa một quân hậu
def only_one_queen_on_column(solver, N):
    for j in range(N):
        exactly_one(solver, [var(i, j, N) for i in range(N)])

# Ràng buộc 3: Mỗi đường chéo tối đa 1 quân hậu
def no_two_queens_on_diagonal(solver, N):
    no_two_queen_on_main_diagonal(solver, N)
    no_two_queen_on_second_diagonal(solver, N)

# Mỗi đường chéo chính tối đa 1 quân hậu
def no_two_queen_on_main_diagonal(solver, N):
    for d in range(-N + 1, N):
        diagonal = [var(i, j, N) for i in range(N) for j in range(N) if (i - j) == d]
        at_most_one(solver, diagonal)

# Mỗi đường chéo phụ tối đa 1 quân hậu
def no_two_queen_on_second_diagonal(solver, N):
    for d in range(0, 2 * N - 1):
        diagonal = [var(i, j, N) for i in range(N) for j in range(N) if (i + j) == d]
        at_most_one(solver, diagonal)

def print_solution(queens, N):
    if not queens:
        print("No solution found!")
        return
    for i in range(N):
        row = ["Q" if (i, j) in queens else "." for j in range(N)]
        print(" ".join(row))

def solve_N_queen(N):
    solver = Glucose3()

    only_one_queen_on_row(solver, N)
    only_one_queen_on_column(solver, N)
    no_two_queens_on_diagonal(solver, N)

    if solver.solve():
        model = solver.get_model()

        queens = []
        for i in range(N):
            for j in range(N):
                if var(i, j, N) in model:
                    queens.append((i, j))

        return queens
    else:
        return None

# Test
N = 8
queens = solve_N_queen(N)
if queens:
    print_solution(queens, N)
else:
    print("No solution found!")
