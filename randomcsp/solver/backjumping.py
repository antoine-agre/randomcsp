from randomcsp.csp import CSP

def generate_ancestors(csp: CSP)-> list[list[int]]:
    ancestors: list[list[int]] = [[] for _ in range(csp.nb_variables)]
    for i in range(csp.nb_variables):
        for j in range(i + 1, csp.nb_variables):
            if csp.constraints[i][j] != None:
                ancestors[j].append(i)
    return ancestors

def generate_domains(csp: CSP)-> list[list[int]]:
    domains: list[list[int]] = [[x for x in range(csp.domain_size)] for _ in range(csp.nb_variables)]
    return domains

def _select_value(csp: CSP, proposed: list[int|None], domain: list[int], i: int):
    # returns coherent x, or None if none exists ; and new domain

    domain = domain.copy()
    proposed = proposed.copy()
    
    while len(domain) > 0:
        x = domain.pop(0)
        proposed[i] = x
        if csp._is_coherent(proposed):
            return x, domain
    return None, domain

def union(set1: list, set2: list):
    output = set1.copy()
    for el in set2:
        if el not in output: output.append(el)
    # output.sort()
    return output

###

def paper_backjumping(csp: CSP):
    ancestors: list[list[int]] = generate_ancestors(csp)
    domains: list[list[int]] = generate_domains(csp)
    i: int = 0
    induced: list[int] = ancestors[i].copy()
    assignation: list[int|None] = [None for _ in range(csp.nb_variables)]

    while 0 <= i < csp.nb_variables:
        
        #select value
        x: int = None
        while len(domains[i]) > 0:
            a: int = domains[i].pop(0)
            assignation[i] = a
            # print("ASSIGNATION :", assignation)
            if csp._is_coherent(assignation):
                x: int = a
                break

        if x == None:
            iprev: int = i
            if len(induced) > 0:
                i = induced.pop(-1)
            else:
                i -= 1
            induced = union(induced, ancestors[i].copy())
            for j in range(i+1, iprev+1): assignation[j] = None
        else:
            i += 1
            if i < csp.nb_variables:
                domains[i] = [x for x in range(csp.domain_size)]
                induced = ancestors[i].copy()
    
    if i == -1:
        return None
    else:
        return assignation
from copy import deepcopy

def iterative_backjumping(csp: CSP):
    i: int = 0
    domains: list[list[int]] = [[] for _ in range(csp.nb_variables)]
    assignation: list[int|None] = [None for _ in range(csp.nb_variables)]
    ancestors: list[list[int]] = generate_ancestors(csp)

    current_ancestors: list[list[int]] = deepcopy(ancestors)#.copy()
    domains[i] = [x for x in range(csp.domain_size)]
    
    while 0 <= i < csp.nb_variables:
        #print("LOOP ; i :", i)
        ok: bool = False
        # print("Sélection d'une valeur cohérente dans le domaine :", domains[i])
        while not ok and len(domains[i]) > 0:
            x: int = domains[i].pop(0)
            # print("\tx :", x)
            assignation[i] = x
            # print("\tassignation :", assignation)
            # print("assignation :", assignation)
            if csp._is_coherent(assignation): ok = True
        
        if not ok: #backjumping
            # print("Pas de x cohérent => backjumping")
            # print("\tAncêtres courants :", current_ancestors[i])
            # print("backjumping")
            iprev: int = i
            # assignation[i] = None
            if len(current_ancestors[i]) > 0:
                # i = current_ancestors.pop(-1)
                i = max(current_ancestors[i])
                # print("\tNouveau i :", i)
                current_ancestors[iprev].remove(i)
            else: #pas de valeurs cohérentes
                # print("\tDEVRAIT ÊTRE INUTILE")
                i -= 1
            
            # print("Nettoyage de l'assignation\n\tAvant :", assignation)
            for j in range(i+1, iprev+1):
                assignation[j] = None
            # print("\tAprès :", assignation)
            
            if i > -1: #ou 0 ?
                current_ancestors[i] = union(current_ancestors[i], current_ancestors[iprev]) #deepcopy(ancestors[i]))
                # print("Nouveaux ancêtres courants :", current_ancestors[i])
        else:
            # print("x cohérent => i +=1")
            # print("i += 1")
            i += 1
            if i < csp.nb_variables:
                domains[i] = [x for x in range(csp.domain_size)]
                # print("Nouveau domaine :", domains[i])
                current_ancestors[i] = deepcopy(ancestors[i])#.copy()
                # print("Ancêtres pris du graphe :", current_ancestors[i])

    # print("Hors de la boucle")
    if i == -1:
        return None
    else:
        return assignation

###

def backjumping(csp: CSP):

    ancestors = generate_ancestors(csp)
    domains = generate_domains(csp)

    # # TODO : push block to generate_ancestors
    # for i in range(len(ancestors)):
    #     if len(ancestors[i]) > 0:
    #         ancestors[i] = ancestors[i][-1]
    #     else:
    #         ancestors[i] = i-1

    print("ancestors :", ancestors)
    print("domains :", domains)

    i:int = 0
    last_i:int = None
    x: int = None
    proposed: list[int|None] = [None for _ in range(csp.nb_variables)]
    I: list[int] = ancestors[0].copy()

    while 0 <= i < csp.nb_variables:
        print("LOOP : i =", i)
        x, domains[i] = _select_value(csp, proposed, domains[i], i)
        print("selected value : x =", x)

        if x is None: #no coherent value => backjumping
            last_i = i

            i = ancestors[i][-1] if len(ancestors[i]) > 0 else i-1
            I = union(I, ancestors[i])
            if i in I: I.remove(i)
            print("backjumping to ancestor : i =", i)
            # if len(ancestors[i]) > 0:
            #     i = ancestors[i][-1]
            #     print("Backjumping to ancestor :", i)
            # else:
            #     i -= 1
            #     print("Backtracking to i-1 :", i)
            
            proposed[i] = None
            for j in range(i + 1, last_i + 1):
                domains[j] = [x for x in range(csp.nb_variables)]
                proposed[j] = None
            print("domains and proposed cleaned :")
            print("\tdomain :", domains)
            print("\tproposed :", proposed)
        else: #x coherent
            proposed[i] = x
            i += 1
            if i < csp.nb_variables: I = ancestors[i].copy()
            print("x coherent with values :", proposed)
            print("going up to i =", i)
    
    print("END OF LOOP")
    if i < 0:
        print("i =", i, ", returning None")
        return None
    else:
        print("i =", i, ", returning proposed :", proposed)
        return proposed

    

# def backjumping(csp: CSP):

#     ancestors = generate_ancestors(csp)
#     domains = generate_domains(csp)

#     print("ancestors :", ancestors)
#     print("domains :", domains)

#     i: int = 0
#     iprev: int|None = None
#     I: list[int] = ancestors[i].copy()
#     proposed: list[int|None] = [None for _ in range(csp.nb_variables)]

#     while 0 <= i < csp.nb_variables:
#         print("proposed =", proposed)
#         print("i =", i)
#         x: int = _select_value(csp, proposed, domains[i], i)
#         print("x =", x)
#         if x is None:
#             print("No coherent x")
#             iprev = i
#             if len(I) == 0: #??
#                 proposed[i] = None
#                 i -= 1
#             else:
#                 for j in range(I[-1]+1, i+1): proposed[j] = None
#                 i = I[-1]
#             I = union(ancestors[i], I)
#             if x in I: I.remove(x)
#         else:
#             print("coherent x")
#             proposed[i] = x
#             print("new proposed =", proposed)
#             i += 1
#             if i < csp.nb_variables: I = ancestors[i].copy()
    
#     if i == -1:
#         return None
#     else:
#         return proposed















# def backjumping(csp: CSP):
#     ancestors = generate_ancestors(csp)
#     domains = generate_domains(csp)

#     i: int = 0
#     proposed: list[int] = [None for _ in range(csp.nb_variables)]
#     #proposed: list[int] = [0 if x == 0 else None for x in range(csp.nb_variables)]

#     while 0 <= i < csp.nb_variables:
#         print("i :", i)

#         if proposed[i] == None:
#             proposed[i] = 0
#         else:
#             proposed[i] += 1

#         print("proposed :", proposed)
        
#         if csp._is_coherent(proposed) and proposed[i] < csp.nb_variables:
#             print("coherent")
#             if not None in proposed:
#                 print("solution found")
#                 return proposed
#             else:
#                 print("i += 1")
#                 i += 1
#         else: #not coherent OR exhausted domain -> backjumping
#             print("backjumping (not coherent or exhausted domain)")
#             if len(ancestors[i]) > 0:
#                 print("jump to ancestor :", ancestors[i][-1])
#                 new_i = ancestors[i][-1]
#             else:
#                 print("chronological :", i-1)
#                 new_i = i - 1
#             for j in range(new_i + 1, i + 1):
#                 proposed[j] = None
#             proposed[new_i] += 1
#             print("new proposed :", proposed)
    
#     return None



def old_backjumping(csp: CSP):
    
    values: list[int] = [0 if x == 0 else None for x in range(csp.nb_variables)]
    ancestors = generate_ancestors(csp)
    domains = generate_domains(csp)
    
    i: int = 0
    Di: list[int] = domains[i].copy()
    # Ii: list[int] = ancestors[i].copy()
    I: list[list[int]] = [ancestors[i].copy() for i in range(csp.nb_variables)]

    while 0 <= i <= csp.nb_variables - 1:
        # x: int = None
        # for value in Di:
        #     values[i] = value
        #     if not csp._is_coherent(values):
        #         Di.remove(value)
        #     else:
        #         break
        ok: bool = False

        while not ok and len(Di) != 0:
            print("Loop")
            x = Di[0]
            print("x :", x)
            Di.pop(0)
            print("Di :", Di)
            values[i] = x
            print("values :", values)
            if csp._is_coherent(values): ok = True
            print("ok :", ok)
        
        if not ok: #x doesn't exist => backjumping
            iprev: int = i
            i = I[i][0]
            I[i] = (I[i] + I[iprev].copy())
            if x in I[i]: I[i].remove(x)
        else:
            print("ok, next step")
            i += 1
            print("i :", i)
            if i < csp.domain_size:
                Di = domains[i].copy()
                print("Di :", Di)
                I[i] = ancestors[i].copy()
                print("I[i] :", I[i])
        
    if i == -1:
        return None
    else:
        return values
        
