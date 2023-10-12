from randomcsp.csp import CSP

def backtracking(csp: CSP):
    #Gaschnig (or naive) backjumping
    i: int = 0
    domains: list[list[int]] = [[] for _ in range(csp.nb_variables)]
    assignation: list[int|None] = [None for _ in range(csp.nb_variables)]

    domains[i] = [x for x in range(csp.domain_size)]

    while 0 <= i < csp.nb_variables:
        ok: bool = False
        while not ok and len(domains[i]) > 0:
            x: int = domains[i].pop(0)
            assignation[i] = x
            if csp.is_coherent(assignation): ok = True
        
        if not ok: #backtracking
            assignation[i] = None
            i -= 1
        else:
            i += 1
            if i < csp.nb_variables: domains[i] = [x for x in range(csp.domain_size)]

    if i == -1:
        return None
    else:
        return assignation

def backtracking_generator(csp: CSP):
    i: int = 0
    domains: list[list[int]] = [[] for _ in range(csp.nb_variables)]
    assignation: list[int|None] = [None for _ in range(csp.nb_variables)]

    domains[i] = [x for x in range(csp.domain_size)]

    while 0 <= i < csp.nb_variables:
        ok: bool = False
        while not ok and len(domains[i]) > 0:
            x: int = domains[i].pop(0)
            assignation[i] = x
            if csp.is_coherent(assignation): ok = True
        
        if not ok: #backtracking
            assignation[i] = None
            i -= 1
        else:
            i += 1
            if i < csp.domain_size: domains[i] = [x for x in range(csp.domain_size)]
            else: #solution
                yield assignation
                i -= 1

    return