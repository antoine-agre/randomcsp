from randomcsp.csp import CSP

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


from randomcsp.solver.backtracking import backtracking, multi_backtracking, iterative_backtracking, iterative_backtracking_generator
from randomcsp.solver.backjumping import iterative_backjumping, paper_backjumping

# count = 0
# # for _ in range(1000):
problem = CSP(5,5)
# problem.generate_constraints(0.5, 0.5)
problem.constraints = [
    [None,None,[(0, 2), (0, 4), (1, 0), (1, 2), (2, 0), (2, 3), (3, 0), (3, 1), (3, 3), (3, 4), (4, 0), (4, 2)],None,[(0, 3), (1, 2), (2, 0), (2, 2), (2, 3), (2, 4), (3, 0), (3, 2), (3, 3), (3, 4), (4, 1), (4, 2)]],
    [None,None,None,[(0, 3), (1, 0), (1, 1), (1, 2), (2, 0), (2, 3), (2, 4), (3, 0), (3, 2), (3, 3), (3, 4), (4, 2)],None],
    [None,None,None,[(0, 1), (0, 4), (1, 0), (1, 1), (1, 2), (1, 4), (2, 0), (3, 0), (3, 4), (4, 0), (4, 1), (4, 3)],[(0, 0), (0, 1), (0, 4), (1, 1), (1, 2), (2, 3), (2, 4), (3, 1), (3, 2), (4, 0), (4, 2), (4, 4)]],
    [None,None,None,None,None],
    [None,None,None,None,None]
    ]

problem.print()

# print("PAPER :", paper_backjumping(problem))

bt = iterative_backtracking(problem)
print("BT :", bt)
bj = iterative_backjumping(problem)
print("BJ :", bj)
if bt != bj:
    print("\tNOT THE SAME RESULT !")
    # problem.print()
    # break
    # count += 1


# nb_queens = 4
# problem = generate_queens(nb_queens)
# print(iterative_backjumping(problem))

count = 0
for i in range(1):
    csp = CSP(12,12)
    csp.generate_constraints(0.5, 0.5)
    bt = iterative_backtracking(csp)
    bj = iterative_backjumping(csp)
    if bt != bj: count += 1
print("BT != BJ COUNT :", count)

# nb_reines = 6
# queens = generate_queens(nb_reines)
# print(iterative_backtracking(queens), "[first solution]")
# solutions = iterative_backtracking_generator(queens)
# count = 0
# for solution in solutions:
#     print(solution)
#     count += 1
# print(count, "solutions")
# print("Problème des", nb_reines, "reines")
# print("Solution :", solution)

# solutions = multi_backtracking(queens)
# print("List :", solutions)
# print(len(solutions), "solutions")

# csp = CSP(5,5)
# csp.generate_constraints(0.5, 0.5)
# from randomcsp.solver.backjumping import backjumping
# bt = backtracking(csp)
# print("Backtracking :", bt)
# bj = backjumping(csp)
# print("Backjumping :", bj)
# print("BT and BJ match :", bt == bj)

# count = 0
# for i in range(1000):
#     # print("\n\n#################\n\n")
#     csp = CSP(5,5)
#     csp.generate_constraints(0.5, 0.5)
#     bt = backtracking(csp)
#     ibt = iterative_backtracking(csp)
#     # bj = backjumping(csp)
#     if bt != ibt:
#         print("NOT MATCHING !")
#         csp.print()
#         print("BT :", bt)
#         print("IBT :", ibt)
#         print("count :", count)
#         break
#     else:
#         count += 1
# print("DONE ! count :", count)