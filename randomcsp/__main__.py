from randomcsp.csp import CSP
from randomcsp.solver.backtracking import backtracking
from randomcsp.solver.backjumping import backjumping
from randomcsp.solver.forwardchecking import forwardchecking
from randomcsp.timer.timer import measure, Parameter, graph
import time

#####

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

DEMO_MODE = False

# Démo

if DEMO_MODE:

    def wait():
        input(f"{'#'*10} Entrée pour continuer. {'#'*10}\n")

    print(f"{'#'*10} Démo {'#'*10}\n")

    print("Génération d'un CSP (6 variables, domaines de taille 6) :")
    csp = CSP(6, 6)
    csp.print()
    print("Génération des contraintes (densité 0.5, dureté 0.5) :")
    csp.generate_constraints(0.5, 0.5)
    csp.print()

    wait()

    print("Recherche d'une solution par les 3 algorithmes :")
    results = backtracking(csp), backjumping(csp), forwardchecking(csp)
    algorithms = ("Backtracking", "Backjumping", "Forward checking")

    for i in range(3):
        print(f"\n{algorithms[i]} :")
        print("\tSolution trouvée :", results[i][0])
        print("\tNombre de backtracks :", results[i][1])
        print("\tNombre de consistency checks :", results[i][2])
    print()

    wait()

    print("Génération et résolution du problème des 4 reines :")

    csp = generate_queens(4)
    csp.print()
    results = backtracking(csp), backjumping(csp), forwardchecking(csp)

    for i in range(3):
        print(f"\n{algorithms[i]} :")
        print("\tSolution trouvée :", results[i][0])
        print("\tNombre de backtracks :", results[i][1])
        print("\tNombre de consistency checks :", results[i][2])
    print()

    wait()

    print("Génération et résolution du problème des 10 reines :")

    csp = generate_queens(10)
    csp.print()
    results = backtracking(csp), backjumping(csp), forwardchecking(csp)

    for i in range(3):
        print(f"\n{algorithms[i]} :")
        print("\tSolution trouvée :", results[i][0])
        print("\tNombre de backtracks :", results[i][1])
        print("\tNombre de consistency checks :", results[i][2])
    print()

    input(f"{'#'*10} Entrée pour quitter la démo. {'#'*10}\n")

    exit(0)

###### Tests

nb_variables_x = [6, 8, 10, 12, 14]
nb_variables_data = measure([backtracking, backjumping, forwardchecking], Parameter.NB_VARIABLES, nb_variables_x)

domain_size_x = [6, 8, 10, 12, 14]
domain_size_data = measure([backtracking, backjumping, forwardchecking], Parameter.DOMAIN_SIZE, domain_size_x)

density_x = [0.2, 0.3, 0.4, 0.5, 0.6]
density_data = measure([backtracking, backjumping, forwardchecking], Parameter.DENSITY, density_x)

tightness_x = [0.2, 0.3, 0.4, 0.5, 0.6]
tightness_data = measure([backtracking, backjumping, forwardchecking], Parameter.TIGHTNESS, tightness_x)

from io import TextIOWrapper

def write_block(file: TextIOWrapper, variable_name: str, x_list: list, data):
    file.write(f"{variable_name}\n")
    file.write("x,")
    for x_value in x_list:
        file.write(str(x_value) + ',')
    file.write("\n")
    for i, measure_type in enumerate(("CPU Time", "Backtracks", "Consistency checks")):
        file.write(measure_type + "\n")
        for j, solver in enumerate(("backtracking", "backjumping", "forward checking")):
            file.write(solver + ",")
            for val in data[i][j]:
                file.write(str(val) + ",")
            file.write("\n")    
        file.write("\n")

with open("output.csv", "w", encoding='UTF8') as file:

    write_block(file, "nb variables", nb_variables_x, nb_variables_data)
    write_block(file, "domain size", domain_size_x, domain_size_data)
    write_block(file, "density", density_x, density_data)
    write_block(file, "tightness", tightness_x, tightness_data)

    file.close()

show: bool = input(
    """Afficher graphes à l'écran ?
Ils seront sauvegardés dans le répertoire graphs/ dans tous les cas. 
(Y/N) : """
) in ['y', 'Y']

for measure_type in ["time", "backtracks", "consistency checks"]:
    graph(measure_type, nb_variables_x, nb_variables_data, "nombre de variables", show)
    graph(measure_type, domain_size_x, domain_size_data, "taille de domaine", show)
    graph(measure_type, density_x, density_data, "densité", show)
    graph(measure_type, tightness_x, tightness_data, "dureté", show)
