from randomcsp.csp import CSP
from copy import deepcopy


def forwardchecking(csp: CSP)-> tuple[list[int]|None, int, int]:
    _backtrack_count: int = 0
    _consistency_check_count: int = 0
    domains: list[list[int]] = [[x for x in range(csp.domain_size)] for _ in range(csp.nb_variables)]
    assignation: list[int|None] = [None for _ in range(csp.nb_variables)]

    i: int = 0

    while 0 <= i < csp.nb_variables:
        ok: bool = False
        
        while not ok and len(domains[i]) > 0:
            x: int = domains[i].pop(0)
            assignation[i] = x
            empty_domain: bool = False
            domains_copy_k = [x.copy() for x in domains]

            for k in range(i+1, csp.nb_variables):
                ## REVISE
                to_remove: list[int] = []
                for a in domains[k]:
                    test_assignation = assignation.copy()
                    test_assignation[k] = a
                    _consistency_check_count += 1
                    if not csp.is_coherent(test_assignation):
                        to_remove.append(a)
                for a in to_remove: domains[k].remove(a)
                ##
                if len(domains[k]) == 0: #TODO : s'arrêter sur un domaine vide
                    empty_domain = True 
                    break # ??
            
            if empty_domain:
                domains = domains_copy_k
            else:
                ok = True
        
        if not ok: #backtrack
            _backtrack_count += 1
            i -= 1
            for j in range(i+1, csp.nb_variables): domains[j] = [x for x in range(csp.domain_size)]
            for j in range(i, csp.nb_variables): assignation[j] = None
        else:
            i += 1
    if i < 0:
        return None, _backtrack_count, _consistency_check_count
    else:
        return assignation, _backtrack_count, _consistency_check_count

