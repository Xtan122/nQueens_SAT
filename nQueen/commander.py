from pysat.solvers import Glucose3
import math


def generate_variables(N):
    # Tạo biến cho mỗi ô trên bàn cờ (1-based indexing)
    return [[i * N + j + 1 for j in range(N)] for i in range(N)]


def generate_commander_variables(start, number_group):
    # Tạo biến commander mới bắt đầu từ start
    return [start + i for i in range(number_group)]


def at_most_one_commander(clauses, variables, start_var):
    n = len(variables)
    if n <= 1:
        return clauses

    # Chia thành các nhóm
    number_group = math.ceil(math.sqrt(n))
    size_of_group = math.ceil(n / number_group)
    commanders = generate_commander_variables(start_var, number_group)
    next_start = start_var + number_group

    # Ràng buộc giữa các commander: tối đa một commander được bật
    for i in range(len(commanders)):
        for j in range(i + 1, len(commanders)):
            clauses.append([-commanders[i], -commanders[j]])

    # Liên kết commander với nhóm
    for i in range(number_group):
        group = variables[i * size_of_group:(i + 1) * size_of_group]
        if group:

            clauses.append([-commanders[i]] + group)

            for j in range(len(group)):
                for k in range(j + 1, len(group)):
                    clauses.append([-commanders[i], -group[j], -group[k]])

            for var in group:
                clauses.append([commanders[i], -var])

    return next_start


def exactly_one_commander(clauses, variables, start_var):
    # Đảm bảo chính xác một biến được chọn
    clauses.append(variables)
    next_start = at_most_one_commander(clauses, variables, start_var)
    return next_start


def generate_clauses(variables, N):
    clauses = []
    max_var = N * N
    start_var = max_var + 1

    # 1. Mỗi hàng có chính xác 1 quân hậu
    for i in range(N):
        start_var = exactly_one_commander(clauses, variables[i], start_var)

    # 2. Mỗi cột có chính xác 1 quân hậu
    for j in range(N):
        col = [variables[i][j] for i in range(N)]
        start_var = exactly_one_commander(clauses, col, start_var)

    # 3. Tối đa 1 quân hậu trên mỗi đường chéo
    for d in range(-N + 1, N):
        diagonal = [variables[i][i + d] for i in range(N) if 0 <= i + d < N]
        if len(diagonal) > 1:
            start_var = at_most_one_commander(clauses, diagonal, start_var)

    # 4. Tối đa 1 quân hậu trên mỗi đường chéo
    for d in range(0, 2 * N - 1):
        diagonal = [variables[i][d - i] for i in range(N) if 0 <= d - i < N]
        if len(diagonal) > 1:
            start_var = at_most_one_commander(clauses, diagonal, start_var)

    return clauses


def solve_N_queens(N):
    variables = generate_variables(N)
    clauses = generate_clauses(variables, N)

    solver = Glucose3()
    for clause in clauses:
        solver.add_clause(clause)

    if solver.solve():
        model = solver.get_model()
        # Chuyển đổi mô hình thành ma trận 2D
        solution = [[0] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                var = variables[i][j] - 1  # Chuyển sang chỉ số 0-based
                if var < len(model) and model[var] > 0:
                    solution[i][j] = 1
        return solution
    return None


def print_solution(solution):
    if solution is None:
        print("Không tìm thấy giải pháp.")
    else:
        for row in solution:
            print(" ".join("Q" if cell else "." for cell in row))


# Chạy thử với N = 4
N = 4
solution = solve_N_queens(N)
print_solution(solution)