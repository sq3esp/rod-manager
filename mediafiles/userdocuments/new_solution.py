import gurobipy as gp
from gurobipy import GRB
import itertools
import random
import time
import math
import numpy as np
from scipy.stats import truncnorm


def prepare_csv():
    write_string = "type;L;R;a0;a1;std_dev_x;x;ro;U;u_max;u_min;p_values;u_values;Q_max;time;\n"
    with open("results.csv", "w") as file:
        file.write(write_string)


def save_results_to_csv(type, L, R, std_dev, x, ro, capacity, u_max, u_min, solution, time):
    write_string = type + ";" + str(L) + ";" + str(R) + ";" + str(a0) + ";" + str(a1) + ";" + str(std_dev) + ";" + \
                   str(x) + ";" + str(ro) + ";" + str(capacity) + ";" + str(u_max) + ";" + str(u_min) + ";" + \
                   str(solution[0]) + ";" + str(solution[1]) + ";" + str(solution[2]) + ";" + str(time) + ";\n"

    with open("results.csv", "a") as file:
        file.write(write_string)


def utility(model, u, a, i):
    if a != 1:
        u_exp = model.addVar(name=f"u_exp_{i}")
        model.addGenConstrPow(u, u_exp, 1 - a, name=f"pow_constr_{i}")
        return (1 - a) ** (-1) * u_exp
    else:
        u_root = model.addVar(name=f"u_root_{i}")
        model.addGenConstrPow(u, u_root, 0.5, name=f"root_constr_{i}")

        return u_root


def optimize_using_solver(L, R, a0, a1, x, ro, u_max, u_min):
    p_values = None
    u_values = None
    Q_max = None

    start = time.time()

    model = gp.Model()

    p = model.addVars(R, vtype=gp.GRB.BINARY, name="p")
    u = model.addVars(R, lb=0, vtype=gp.GRB.CONTINUOUS, name="u")

    model.update()

    model.setObjective(gp.quicksum(p[r] * x[r] * utility(model, u[r], a1, r) for r in range(R)) -
                       gp.quicksum(a0 * (1 - p[r]) for r in range(R)), gp.GRB.MAXIMIZE)

    for l in range(L):
        model.addConstr(gp.quicksum(p[r] * ro[l][r] * u[r] for r in range(R)) <= U[l], name=f"Sum_Constraint_{l}")

    for r in range(R):
        model.addConstr(u[r] <= (p[r] * u_max[r]), name=f"Max_Constraint_{r}")
        model.addConstr(u[r] >= (p[r] * u_min[r]), name=f"Min_Constraint_{r}")

    model.update()

    model.optimize()

    if model.status == gp.GRB.OPTIMAL:
        p_values = model.getAttr('X', p)
        u_values = model.getAttr('X', u)
        Q_max = model.ObjVal

    end = time.time()
    total_time = end - start
    print(f"Czas: {total_time} s")

    found_max = [p_values, u_values, Q_max]

    print("Optymalne wartości dla p:", p_values)
    print("Optymalne wartości dla u:", u_values)
    return [found_max, total_time]


def optimize_using_algorithm(all_p_combinations, L, R, a0, a1, x, ro, u_max, u_min):
    results = []
    start = time.time()

    for p_combination in all_p_combinations:
        model = gp.Model("NLP")
        u = model.addVars(R, lb=0, vtype=GRB.CONTINUOUS, name="u")

        # Dodawanie ograniczeń dla zmiennych u
        for r in range(R):
            model.addConstr(u[r] <= u_max[r], name=f"u_max_constr_{r}")
            model.addConstr(u[r] >= u_min[r], name=f"u_min_constr_{r}")

        # Dodawanie ograniczeń przepustowości na połączenia
        for l in range(L):
            model.addConstr(gp.quicksum(p_combination[r] * ro[l][r] * u[r] for r in range(R)) <= U[l],
                            name=f"Sum_Constraint_{l}")

        # Aktualizacja modelu po dodaniu zmiennych i ograniczeń
        model.update()

        # Obliczanie wartości funkcji użyteczności i celu
        obj = gp.quicksum(p_combination[r] * x[r] * utility(model, u[r], a1, r) for r in range(R)) - gp.quicksum(
            a0 * (1 - p_combination[r]) for r in range(R))

        model.setObjective(obj, GRB.MAXIMIZE)

        model.optimize()

        if model.status == GRB.OPTIMAL:
            p_values = p_combination
            u_values = model.getAttr('X', u)
            Q_max = model.ObjVal
            solution = {r: u_values[r] for r in range(R)}
            results.append([p_values, solution, Q_max])

    end = time.time()
    total_time = end - start
    print(f"Czas: {end - start} s")

    if len(results) == 0:
        return [["None", "None", "None"], total_time]

    found_max = max(results, key=lambda x: x[-1])

    print("Optymalne wartości dla p:", found_max[0])
    print("Optymalne wartości dla u:", found_max[1])

    return [found_max, total_time]


def network_matrix_generator(L, R):
    ro = [[random.randint(0, 1) for _ in range(R)] for _ in range(L)]

    for i in range(L):
        if sum(ro[i]) == 0:
            # Wybierz losowe połączenie w tabeli i ustaw je na 1
            j = random.randint(0, R - 1)
            ro[i][j] = 1

    return ro


def capacity_generator(length, min, max):
    return [math.floor(random.randint(min, max) / 10) * 10 for _ in range(length)]


def normalize_wages(random_values):
    total_sum = sum(random_values)
    return [value / total_sum for value in random_values]


def truncated_normal_distribution(mean=0, std=1, lbound=0, ubound=1, size=1000):
    # Przekształcenie low i high na znormalizowane granice
    a, b = (lbound - mean) / std, (ubound - mean) / std
    # Generowanie próbek z uciętego rozkładu normalnego
    samples = truncnorm.rvs(a, b, loc=mean, scale=std, size=size)
    return samples.tolist()


def round_all(list):
    return [round(x) for x in list]


# kara
a0 = 2
# parametr do utility -> na sztywno 0.5
a1 = 0.5

L = [3, 4, 5]
R = [5, 7, 9]
standard_deviation_x = [0.5, 2, 6]

# min max capacities
caps = [50, 80]

# minimum speeds for demands
mins = [10, 30]

# max speeds for demands
maxs = [mins[1], 100]

problems = []


prepare_csv()
for l in L:
    for r in R:
        for std in standard_deviation_x:
            U = round_all(
                truncated_normal_distribution(mean=float(np.mean(caps)), std=5, lbound=caps[0], ubound=caps[1], size=l))
            u_min = round_all(
                truncated_normal_distribution(mean=float(np.mean(mins)), std=4, lbound=mins[0], ubound=mins[1],
                                              size=r))
            u_max = round_all(
                truncated_normal_distribution(mean=float(np.mean(maxs)), std=10, lbound=maxs[0], ubound=maxs[1],
                                              size=r))

            x = normalize_wages(truncated_normal_distribution(mean=10, std=std, lbound=0, ubound=20, size=r))
            all_p_combinations = list(itertools.product([0, 1], repeat=r))

            for i in range(3):
                ro = network_matrix_generator(l, r)
                solver_solution = optimize_using_solver(l, r, a0, a1, x, ro, u_max, u_min)
                save_results_to_csv(type="Solver", L=l, R=r, std_dev=std, x=x, ro=ro, capacity=U, u_max=u_max,
                                    u_min=u_min,
                                    solution=solver_solution[0], time=solver_solution[1])

                algorithm_solution = optimize_using_algorithm(all_p_combinations, l, r, a0, a1, x, ro, u_max, u_min)
                save_results_to_csv(type="Algorithm", L=l, R=r, std_dev=std, x=x, ro=ro, capacity=U, u_max=u_max,
                                    u_min=u_min,
                                    solution=algorithm_solution[0], time=algorithm_solution[1])
