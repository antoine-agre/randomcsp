from randomcsp.csp import CSP
from randomcsp.solver.backtracking import backtracking
from randomcsp.solver.backjumping import backjumping

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


# problem.constraints = [
#     [None,None,[(0, 2), (0, 4), (1, 0), (1, 2), (2, 0), (2, 3), (3, 0), (3, 1), (3, 3), (3, 4), (4, 0), (4, 2)],None,[(0, 3), (1, 2), (2, 0), (2, 2), (2, 3), (2, 4), (3, 0), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2)]],
#     [None,None,None,[(0, 3), (1, 0), (1, 1), (1, 2), (2, 0), (2, 3), (2, 4), (3, 0), (3, 2), (3, 3), (3, 4), (4, 2)],None],
#     [None,None,None,[(0, 1), (0, 4), (1, 0), (1, 1), (1, 2), (1, 4), (2, 0), (3, 0), (3, 4), (4, 0), (4, 1), (4, 3)],[(0, 0), (0, 1), (0, 4), (1, 1), (1, 2), (2, 3), (2, 4), (3, 1), (3, 2), (4, 0), (4, 2), (4, 4)]],
#     [None,None,None,None,None],
#     [None,None,None,None,None]
#     ]

# problem.print()

# bt = backtracking(problem)
# print("BT :", bt)
# bj = backjumping(problem)
# print("BJ :", bj)
# if bt != bj:
#     print("\tNOT THE SAME RESULT !")
# count = 0
# for i in range(1):
#     csp = CSP(12,12)
#     csp.generate_constraints(0.5, 0.5)
#     bt = backtracking(csp)
#     bj = backjumping(csp)
#     if bt != bj: count += 1
# print("BT != BJ COUNT :", count)

################

# Timing : 
# time.perf_counter() : wall time, arbitrary so more precise than epoch-related timing
# time.process_time() : CPU time

import time

csp = CSP(12, 12)
csp.generate_constraints(0.5, 0.5)

average_wall_time = 0
average_cpu_time = 0

loops = 10

for i in range(loops):

    cpu_start = time.process_time()
    wall_start = time.perf_counter()
    backtracking(csp)
    wall_end = time.perf_counter()
    cpu_end = time.process_time()

    cpu_delta = cpu_end - cpu_start
    wall_delta = wall_end - wall_start
    average_cpu_time += cpu_delta
    average_wall_time += wall_delta

    print(f"[{i}]")
    print("\tCPU :", cpu_delta)
    print("\tWall :", wall_delta)
print("\n")

average_cpu_time = average_cpu_time / loops
average_wall_time = average_wall_time / loops
print("Average CPU :", average_cpu_time)
print("Average Wall :", average_wall_time)


for i in range(16,17+1):
    queens = generate_queens(i)
    print(f"Problème des {i} reines")
    average = 0
    for j in range(5):
        time_start = time.process_time()
        backjumping(queens)
        average += time.process_time() - time_start
    average = average / 5
    print("\tAverage CPU time :", average)