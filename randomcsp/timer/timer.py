import time
import matplotlib as plt
from enum import Enum
from randomcsp.csp import CSP
import math

class Parameter(Enum):
    NB_VARIABLES = 1
    DOMAIN_SIZE = 2
    DENSITY = 3
    TIGHTNESS = 4

def measure(solvers: list[callable], tested_parameter: Parameter, parameter_values: list[int|float])-> list[list[list[float]], list[list[float]]]:
    """Given a solver function, computes data points by generating 5 CSPs 
    and solving each of them 5 times, averaging all results.
    The tested parameter is trier for each value provided, while the others 
    have default values.

    Args:
        solvers (list[callable]): The solver functions to measure.
        tested_parameter (Parameter): The parameter that is going to take all values provided.
        values (list[int|float]): The values provided.

    Returns:
        list[list[list[float]], list[list[float]]]: The data points : [Wall/CPU][solver][data points]
    """
    
    # Parameter values
    nb_variables: int = 10
    domain_size: int = 10
    density: float = 0.4
    tightness: float = 0.4

    parameters: list[int|float] = [nb_variables, domain_size, density, tightness]

    match tested_parameter:
        case Parameter.NB_VARIABLES:
            parameter_index = 0
        case Parameter.DOMAIN_SIZE:
            parameter_index = 1
        case Parameter.DENSITY:
            parameter_index = 2
        case Parameter.TIGHTNESS:
            parameter_index = 3
        case _:
            raise Exception("tested_parameter not matching.")

    # Data

    data: list[list[list[float]]] = [[[] for _ in range(len(solvers))] for _ in range(2)]
    
    # Measure
    for value in parameter_values:
        
        parameters[parameter_index] = value

        CSP_MEASURES = 5
        csp_wall_time = [0 for _ in solvers]
        csp_cpu_time = [0 for _ in solvers]

        for csp_index in range(CSP_MEASURES):

            csp: CSP = CSP(parameters[0], parameters[1])
            csp.generate_constraints(parameters[2], parameters[3])
            
            for i, solver in enumerate(solvers):

                TIME_MEASURES = 5
                wall_time = 0
                cpu_time = 0

                for _ in range(TIME_MEASURES):
                    cpu_start = time.process_time()
                    wall_start = time.perf_counter()
                    print("SOLUTION :", solver(csp))
                    wall_end = time.perf_counter()
                    cpu_end = time.process_time()

                    wall_time += wall_end - wall_start
                    cpu_time += cpu_end - cpu_start

                    print(".", end="")
                
                print(csp_index, f"/ {CSP_MEASURES} ...")

                wall_time = wall_time / TIME_MEASURES
                cpu_time = cpu_time / TIME_MEASURES

                csp_wall_time[i] += wall_time
                csp_cpu_time[i] += cpu_time
                

        csp_wall_time = [x / CSP_MEASURES for x in csp_wall_time]
        csp_cpu_time = [x / CSP_MEASURES for x in csp_cpu_time]

        for j in range(len(solvers)):
            data[0][j].append(csp_wall_time[j])
            data[1][j].append(csp_cpu_time[j])
    
    return data

# def progress(val, max, segment_amount = 10):

#     if val == 0:
#         return(' ' * segment_amount)


#     segment_size = max(0, (int(max/segment_amount)))
#     full = int(val//segment_size)
#     rest = val - full*segment_size
#     rest = math.floor((rest/segment_size)*4)

#     out = ""
#     out += '█' * full
#     if val < max:
#         if rest == 0:
#             out += ' '
#         elif rest == 1:
#             out += '░'
#         elif rest == 2:
#             out += '▒'
#         elif rest == 3:
#             out += '▓'
#         else:
#             out += '?'
#     out += ' ' * (segment_amount-full-1)
#     return out