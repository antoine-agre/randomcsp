from randomcsp.csp import CSP

def iterative_backtracking(csp: CSP):
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
            # print("assignation :", assignation)
            if csp._is_coherent(assignation): ok = True
        
        if not ok: #backtracking
            # print("backtracking")
            assignation[i] = None
            i -= 1
        else:
            # print("i += 1")
            i += 1
            if i < csp.domain_size: domains[i] = [x for x in range(csp.domain_size)]

    if i == -1:
        return None
    else:
        return assignation

def iterative_backtracking_generator(csp: CSP):
    i: int = 0
    domains: list[list[int]] = [[] for _ in range(csp.nb_variables)]
    assignation: list[int|None] = [None for _ in range(csp.nb_variables)]

    domains[i] = [x for x in range(csp.domain_size)]

    while 0 <= i < csp.nb_variables:
        ok: bool = False
        while not ok and len(domains[i]) > 0:
            x: int = domains[i].pop(0)
            assignation[i] = x
            # print("assignation :", assignation)
            if csp._is_coherent(assignation): ok = True
        
        if not ok: #backtracking
            # print("backtracking")
            assignation[i] = None
            i -= 1
        else:
            # print("i += 1")
            i += 1
            if i < csp.domain_size: domains[i] = [x for x in range(csp.domain_size)]
            else: #solution
                yield assignation
                i -= 1

    return
    # if i == -1:
    #     return None
    # else:
    #     yield assignation


###

def backtracking(csp: CSP, candidate: list[int|None] = None, indent = 0)-> list[int]|None:
    """Recherche une solution cohérente par backtracking.

    Args:
        candidate (list[int | None], optional): Valeurs proposées. Defaults to None.
        indent (int, optional): Indentation des affichages. Defaults to 0.

    Returns:
        list[int]|None: La liste des valeurs des variables pour une solution trouvée, ou None si aucune solution n'a été trouvée.
    """

    if candidate == None:
        candidate = [0 if x == 0 else None for x in range(csp.nb_variables)]

    # print('\t'*indent + "New backtracking :", candidate)

    while candidate != None:

        if csp._is_coherent(candidate):
            if not None in candidate:
                # print('\t'*indent + "Candidate coherent and full.")
                return candidate
            else:
                # print('\t'*indent + "Candidate coherent but not full.")
                backtrack = backtracking(csp, csp._extend(candidate), indent = indent + 1)
                # print('\t'*indent + "Return value :", backtrack)
                if backtrack != None: return backtrack

        # print('\t'*indent + "Candidate", candidate, "not coherent.")
        candidate = csp._next(candidate)
        # print('\t'*indent + "Next candidate :", candidate)
    
    return None

def multi_backtracking(csp: CSP, candidate: list[int|None] = None, _recursive = False, indent = 0)-> list[int]|None:
    """Recherche une solution cohérente par backtracking.

    Args:
        candidate (list[int | None], optional): Valeurs proposées. Defaults to None.
        indent (int, optional): Indentation des affichages. Defaults to 0.

    Returns:
        list[int]|None: La liste des valeurs des variables pour une solution trouvée, ou None si aucune solution n'a été trouvée.
    """

    if candidate == None and _recursive == False:
        candidate = [0 if x == 0 else None for x in range(csp.nb_variables)]

    out = []

    # print('\t'*indent + "New backtracking :", candidate)

    while candidate != None:

        if csp._is_coherent(candidate):
            if not None in candidate:
                # print('\t'*indent + "Candidate coherent and full.")
                out += [candidate]
            # print('\t'*indent + "Candidate coherent but not full.")
            backtrack = multi_backtracking(csp, csp._extend(candidate), _recursive = True, indent = indent + 1)
            # print('\t'*indent + "Return value :", backtrack)
            if backtrack != None: out += backtrack

        # print('\t'*indent + "Candidate", candidate, "not coherent.")
        candidate = csp._next(candidate)
        # print('\t'*indent + "Next candidate :", candidate)
    
    return out