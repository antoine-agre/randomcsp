from randomcsp.csp import CSP
from copy import deepcopy

"""

i = 0
tant que 0 <= i < n:
    tester toutes les valeurs x du domaine de i
        vérifier cohérence avec les variables suivantes
        si domaine vide : valeur incohérente
        sinon : continuer
"""

def forwardchecking(csp: CSP)-> list[int]|None:
    domains: list[list[int]] = [[x for x in range(csp.domain_size)] for _ in range(csp.nb_variables)]
    assignation: list[int|None] = [None for _ in range(csp.nb_variables)]

    i: int = 0

    while 0 <= i < csp.nb_variables:
        ok: bool = False
        # domains_copy_i: list[list[int]] = deepcopy(domains)
        #print("\ni =", i)

        while not ok and len(domains[i]) > 0:
            x: int = domains[i].pop(0)
            assignation[i] = x
            #print("x =", x, "; assignation =", assignation)
            #print("domains :", domains)
            empty_domain: bool = False
            domains_copy_k: list[list[int]] = deepcopy(domains)

            for k in range(i+1, csp.nb_variables):
                #print("\tk =", k)
                ## REVISE
                to_remove: list[int] = []
                for a in domains[k]:
                    test_assignation = deepcopy(assignation)
                    test_assignation[k] = a
                    if not csp.is_coherent(test_assignation):
                        to_remove.append(a)
                for a in to_remove: domains[k].remove(a)
                #print("\tnew domain for k :", domains[k])
                ##
                if len(domains[k]) == 0: #TODO : s'arrêter sur un domaine vide
                    empty_domain = True 
                    break # ??
            
            if empty_domain:
                #print("empty domain.")
                #print("old domain :", domains)
                domains = domains_copy_k
                #print("new domains :", domains)
            else:
                #print("no empty domain.")
                ok = True
        
        if not ok: #backtrack
            #print("backtrack")
            # domains = domains_copy_i
            i -= 1
            for j in range(i+1, csp.nb_variables): domains[j] = [x for x in range(csp.domain_size)]
            for j in range(i, csp.nb_variables): assignation[j] = None
        else:
            #print("i += 1")
            i += 1
    if i < 0:
        return None
    else:
        return assignation
