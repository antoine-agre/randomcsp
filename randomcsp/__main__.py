from randomcsp.csp import CSP
from randomcsp.solver.backtracking import backtracking
from randomcsp.solver.backjumping import backjumping
from randomcsp.solver.forwardchecking import forwardchecking
from randomcsp.timer.timer import measure, Parameter
import matplotlib.pyplot as plt

def generate_queens(n: int)-> CSP:
    csp = CSP(n, n)
    
    for left_variable in range(n):
        for right_variable in range(left_variable + 1, n):
            difference = right_variable - left_variable
            couples = []
            for left_value in range(n):
                possible_right_values = [x for x in range(n)]
                possible_right_values.remove(left_value)
                if left_value + difference in possible_right_values:
                    possible_right_values.remove(left_value + difference)
                if left_value - difference in possible_right_values:
                    possible_right_values.remove(left_value - difference)

                for right_value in possible_right_values:
                    couples.append((left_value, right_value))
            csp.constraints[left_variable][right_variable] = couples

    
    return csp





###### Graphs

def graph(time_type: str, x_values: list, data, variable_name: str):

    match time_type:
        case "wall":
            time_index = 0
        case "cpu":
            time_index = 1
        case _:
            raise Exception("time_type not recognized.")

    x = x_values
    y0 = data[time_index][0]
    y1 = data[time_index][1]
    y2 = data[time_index][2]

    plt.title(f"Temps de résolution moyen par rapport à [{variable_name}], {time_type} time")
    plt.plot(x, y0, label = "Backtracking")
    plt.plot(x, y1, label = "Backjumping")
    plt.plot(x, y2, label = "Forward checking")
    # plt.bar([x-0.2 for x in x], y0, width=0.2, label = "Backtracking")
    # plt.bar(x, y1, width=0.2, label = "Backjumping")
    # plt.bar([x+0.2 for x in x], y2, width=0.2, label = "Forward checking")
    plt.xticks(x)
    plt.legend()
    plt.xlabel(variable_name.capitalize())
    plt.ylabel("Temps moyen de résolution")
    plt.show()

x = [6,8,10,12]
data = measure([backtracking, backjumping, forwardchecking], Parameter.NB_VARIABLES, x)

for time_type in ["wall", "cpu"]:
    graph(time_type, x, data, "nombre de variables")

input("Entrée pour fermer la fenêtre.")

# queens = generate_queens(4)
# print("BT :", backtracking(queens))
# print("BJ :", backjumping(queens))
# print("FC :", forwardchecking(queens))

# count = 0
# print("\n")
# for i in range(1, 101):
#     print(f"\r[{progress(i, 100, 48)}]", end = "")
#     csp = CSP(16, 10)
#     csp.generate_constraints(0.2, 0.20)
#     bt = backtracking(csp)
#     # print(bt)
#     bj = backjumping(csp)
#     # print(bj)
#     fc = forwardchecking(csp)
#     # print(fc)
#     if bt == bj == fc:
#         # print("SAME :", fc)
#         pass
#     else:
#         # print("DIFFERENT :", bt, bj, fc)
#         count += 1
# print("\n")
# print("\ndifferent count :", count)