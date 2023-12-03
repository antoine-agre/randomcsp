import time
import matplotlib as plt
from enum import Enum
from randomcsp.csp import CSP
import math
from randomcsp.solver.forwardchecking import forwardchecking
import matplotlib.pyplot as plt
import os

class Parameter(Enum):
    NB_VARIABLES = 1
    DOMAIN_SIZE = 2
    DENSITY = 3
    TIGHTNESS = 4

def measure(solvers: list[callable], tested_parameter: Parameter, parameter_values: list[int|float])-> list[list[list[float]]]:
    """Given a solver function, computes data points by generating 5 CSPs 
    and solving each of them 5 times, averaging all results.
    The tested parameter is tried for each value provided, while the others 
    have default values.

    Args:
        solvers (list[callable]): The solver functions to measure.
        tested_parameter (Parameter): The parameter that is going to take all values provided.
        values (list[int|float]): The values provided.

    Returns:
        list[list[list[float]]]: The data points : [measure type][solver][data points]
    """
    
    # Default parameter values
    nb_variables: int = 10
    domain_size: int = 10
    density: float = 0.3
    tightness: float = 0.7

    parameters: list[int|float] = [nb_variables, domain_size, density, tightness]

    print("\nParameter : ", end="")
    match tested_parameter:
        case Parameter.NB_VARIABLES:
            parameter_index = 0
            print("nb. of variables")
        case Parameter.DOMAIN_SIZE:
            parameter_index = 1
            print("domain size")
        case Parameter.DENSITY:
            parameter_index = 2
            print("density")
        case Parameter.TIGHTNESS:
            parameter_index = 3
            print("tightness")
        case _:
            raise Exception("tested_parameter not matching.")

    # Data

    data: list[list[list[float]]] = [[[] for _ in range(len(solvers))] for _ in range(3)]
    
    # Measure
    for value in parameter_values:
        
        parameters[parameter_index] = value
        print("Value :", value)

        CSP_MEASURES = 5
        # csp_wall_time = [0 for _ in solvers]
        csp_cpu_time = [0 for _ in solvers]
        csp_backtracks = [0 for _ in solvers]
        csp_consistency_checks = [0 for _ in solvers]

        print("CSP\tSolver\tProgress")

        for csp_index in range(CSP_MEASURES):

            csp: CSP = CSP(parameters[0], parameters[1])
            csp.generate_constraints(parameters[2], parameters[3])

            # Regenerate CSP if no solution exists
            while forwardchecking(csp)[0] == None:
                csp = CSP(parameters[0], parameters[1])
                csp.generate_constraints(parameters[2], parameters[3])
            
            # print(f"{csp_index+1}/{CSP_MEASURES}\t", end="") #!#
            
            for i, solver in enumerate(solvers):

                TIME_MEASURES = 5
                # wall_time = 0
                cpu_time = 0
                backtracks = 0
                consistency_checks = 0

                print(f"\r{csp_index+1}/{CSP_MEASURES}\t{i+1}/{len(solvers)}\t", end="")

                for _ in range(TIME_MEASURES):
                    cpu_start = time.process_time()
                    # wall_start = time.perf_counter()
                    _output = solver(csp)
                    # wall_end = time.perf_counter()
                    cpu_end = time.process_time()
                    # print("SOLUTION :", _output[0])

                    # wall_time += wall_end - wall_start
                    cpu_time += cpu_end - cpu_start
                    backtracks += _output[1]
                    consistency_checks += _output[2]

                    print("█", end="")
                
                if i != len(solvers) - 1 or csp_index != CSP_MEASURES - 1:
                    print("\n" + '\033[1A', end='\x1b[2K')
                
                # print("\n")
                # print('\033[1A', end='\x1b[2K')

                # wall_time = wall_time / TIME_MEASURES
                cpu_time = cpu_time / TIME_MEASURES
                backtracks = backtracks / TIME_MEASURES
                consistency_checks = consistency_checks / TIME_MEASURES

                # csp_wall_time[i] += wall_time
                csp_cpu_time[i] += cpu_time
                csp_backtracks[i] += backtracks
                csp_consistency_checks[i] += consistency_checks

            # if csp_index == CSP_MEASURES - 1:
            #     print()
                
        print("\n")

        # csp_wall_time = [x / CSP_MEASURES for x in csp_wall_time]
        csp_cpu_time = [x / CSP_MEASURES for x in csp_cpu_time]
        csp_backtracks = [x / CSP_MEASURES for x in csp_backtracks]
        csp_consistency_checks = [x / CSP_MEASURES for x in csp_consistency_checks]

        for j in range(len(solvers)):
            # data[0][j].append(csp_wall_time[j])
            data[0][j].append(csp_cpu_time[j])
            data[1][j].append(csp_backtracks[j])
            data[2][j].append(csp_consistency_checks[j])
    
    return data

def graph(measure_type: str, x_values: list, data, variable_name: str, show: bool):
    """Shows a graph from data obtained using timer.measure().

    Args:
        measure_type (str): Measure type, "time", "backtracks", or "consistency checks"
        x_values (list): Values of parameter to test against
        data (_type_): Data to pull from, generated by timer.measure()
        variable_name (str): Name of the tested parameter, to show in title

    Raises:
        Exception: measure_type not recognized
    """

    match measure_type:
        case "time":
            measure_index = 0
        case "backtracks":
            measure_index = 1
        case "consistency checks":
            measure_index = 2
        case _:
            raise Exception("measure_type not recognized.")

    x = x_values
    y0 = data[measure_index][0]
    y1 = data[measure_index][1]
    y2 = data[measure_index][2]

    plt.title(f"Temps de résolution moyen par rapport à [{variable_name}]\nMesure : {measure_type}")
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

    # dir = os.path.dirname(__file__)
    # dir = os.path.join(dir, "graphs/")

    if not os.path.isdir("graphs"):
        os.makedirs("graphs")

    save_dir = os.path.join("graphs", f"{variable_name.replace(' ', '_')}-{measure_type.replace(' ', '_')}.png")

    plt.savefig(save_dir)
    if show: plt.show()
    else: plt.clf()
