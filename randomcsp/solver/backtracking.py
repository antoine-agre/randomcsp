from randomcsp.csp import CSP

def backtracking(csp: CSP)-> tuple[list[int]|None, int, int]:
    _backtrack_count: int = 0
    _consistency_check_count: int = 0
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
            _consistency_check_count += 1
            if csp.is_coherent(assignation): ok = True
        
        if not ok: #backtracking
            _backtrack_count += 1
            assignation[i] = None
            i -= 1
        else:
            i += 1
            if i < csp.nb_variables: domains[i] = [x for x in range(csp.domain_size)]

    if i == -1:
        return None, _backtrack_count, _consistency_check_count
    else:
        return assignation, _backtrack_count, _consistency_check_count

