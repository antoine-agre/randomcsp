from randomcsp.csp import CSP
from randomcsp.solver.backtracking import backtracking
from randomcsp.solver.backjumping import backjumping
from randomcsp.solver.forwardchecking import forwardchecking

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



# import time

# csp = CSP(12, 12)
# csp.generate_constraints(0.5, 0.5)

# average_wall_time = 0
# average_cpu_time = 0

# loops = 10

# for i in range(loops):

#     cpu_start = time.process_time()
#     wall_start = time.perf_counter()
#     backtracking(csp)
#     wall_end = time.perf_counter()
#     cpu_end = time.process_time()

#     cpu_delta = cpu_end - cpu_start
#     wall_delta = wall_end - wall_start
#     average_cpu_time += cpu_delta
#     average_wall_time += wall_delta

#     print(f"[{i}]")
#     print("\tCPU :", cpu_delta)
#     print("\tWall :", wall_delta)
# print("\n")

# average_cpu_time = average_cpu_time / loops
# average_wall_time = average_wall_time / loops
# print("Average CPU :", average_cpu_time)
# print("Average Wall :", average_wall_time)


# for i in range(16,17+1):
#     queens = generate_queens(i)
#     print(f"Problème des {i} reines")
#     average = 0
#     for j in range(5):
#         time_start = time.process_time()
#         print(backjumping(queens))
#         average += time.process_time() - time_start
#     average = average / 5
#     print("\tAverage CPU time :", average)

queens = generate_queens(4)
print("BT :", backtracking(queens))
print("BJ :", backjumping(queens))
print("FC :", forwardchecking(queens))

import math
def progress(val, max, segment_amount = 10):
    segment_size = int(max/segment_amount)
    full = int(val//segment_size)
    rest = val - full*segment_size
    rest = math.floor((rest/segment_size)*4)

    out = ""
    out += '█' * full
    if val < max:
        if rest == 0:
            out += ' '
        elif rest == 1:
            out += '░'
        elif rest == 2:
            out += '▒'
        elif rest == 3:
            out += '▓'
        else:
            out += '?'
    out += ' ' * (segment_amount-full-1)
    return out

count = 0
print("\n")
for i in range(1, 101):
    print(f"\r[{progress(i, 100, 48)}]", end = "")
    csp = CSP(16, 10)
    csp.generate_constraints(0.2, 0.20)
    bt = backtracking(csp)
    # print(bt)
    bj = backjumping(csp)
    # print(bj)
    fc = forwardchecking(csp)
    # print(fc)
    if bt == bj == fc:
        # print("SAME :", fc)
        pass
    else:
        # print("DIFFERENT :", bt, bj, fc)
        count += 1
print("\n")
print("\ndifferent count :", count)


# from time import perf_counter, process_time

# cpu_start = process_time()
# wall_start = perf_counter()
# print(backtracking(generate_queens(21)))
# wall_end = perf_counter()
# cpu_end = process_time()
# print("Wall time :", wall_end - wall_start)
# print("CPU time :", cpu_end - cpu_start)