from randomcsp.csp import CSP
from copy import deepcopy

def _generate_ancestors(csp: CSP)-> list[list[int]]:
    ancestors: list[list[int]] = [[] for _ in range(csp.nb_variables)]
    for i in range(csp.nb_variables):
        for j in range(i + 1, csp.nb_variables):
            if csp.constraints[i][j] != None:
                ancestors[j].append(i)
    return ancestors

def _generate_domains(csp: CSP)-> list[list[int]]:
    domains: list[list[int]] = [[x for x in range(csp.domain_size)] for _ in range(csp.nb_variables)]
    return domains

def _union(set1: list, set2: list):
    output = set1.copy()
    for el in set2:
        if el not in output: output.append(el)
    # output.sort()
    return output



def backjumping(csp: CSP):
    i: int = 0
    domains: list[list[int]] = [[] for _ in range(csp.nb_variables)]
    assignation: list[int|None] = [None for _ in range(csp.nb_variables)]
    ancestors: list[list[int]] = _generate_ancestors(csp)

    current_ancestors: list[list[int]] = deepcopy(ancestors)
    domains[i] = [x for x in range(csp.domain_size)]
    
    while 0 <= i < csp.nb_variables:
        ok: bool = False
        while not ok and len(domains[i]) > 0:
            x: int = domains[i].pop(0)
            assignation[i] = x
            if csp.is_coherent(assignation): ok = True
        
        if not ok: #backjumping
            iprev: int = i
            if len(current_ancestors[i]) > 0:
                i = max(current_ancestors[i])
                current_ancestors[iprev].remove(i)
            else: #pas de valeurs cohérentes
                i -= 1
            
            for j in range(i+1, iprev+1):
                assignation[j] = None
            
            if i > -1:
                current_ancestors[i] = _union(current_ancestors[i], current_ancestors[iprev])
        else:
            i += 1
            if i < csp.nb_variables:
                domains[i] = [x for x in range(csp.domain_size)]
                current_ancestors[i] = deepcopy(ancestors[i])

    if i == -1:
        return None
    else:
        return assignation
