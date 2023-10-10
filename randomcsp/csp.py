import random
import math

class CSP:

    ## Constraints : on utilise toujours (i,j) avec i < j

    def __init__(self, nb_variables: int, domain_size: int) -> None:
        """Génère un CSP (Constraint Satisfaction Problem) sans contraintes

        Args:
            nb_variables (int): Le nombre de variables du CSP.
            domain_size (int): La taille du domaine de chaque variable.
        """

        self.nb_variables: int = nb_variables
        self.domain_size: int = domain_size
        # self.domains: list[int] = []
        self.constraints: list[list[list[tuple[int, int]]|None]] = []

        for i in range(nb_variables):
            # self.domains.append(random.randint(2, self.domain_size))
            self.constraints.append([])
            for j in range(nb_variables):
                self.constraints[i].append(None)
    
    def generate_constraints(self, density: float, durete: float)-> None:
        """Génère des contraintes selon les paramètres de densité et de dureté.

        Args:
            density (float): Dans [0;1], proportion des couples de variables qui doivent posséder une contrainte.
            durete (float): Dans [0;1] ; pour toutes les contraintes, proportion des couples de valeurs possibles qui seront autorisées.0
        """

        # Calcul du nombre de contraintes
        nb_constraints = math.floor(density * ((self.nb_variables * (self.nb_variables - 1)) / 2))

        # Définition des couples de variables possibles
        possible_pairings: list[tuple[int, int]] = [] #couples de variables
        for i in range(self.nb_variables):
            for j in range(i+1, self.nb_variables):
                possible_pairings.append((i,j))
        
        # Tirage des couples de variables qui auront une contrainte
        pairings: list[tuple[int, int]] = []
        for i in range(nb_constraints):
            pairings.append(possible_pairings.pop(random.randint(0, len(possible_pairings) - 1)))
        
        # Création des contraintes
        for pairing in pairings:

            # On fait toujours référence aux variables d'un couple dans l'ordre croissant
            first_var = min(pairing)
            second_var = max(pairing)

            # Calcul du nombre de couples de valeurs
            ##nb_couples: int = max(1, math.floor(durete * (self.domains[first_var] * self.domains[second_var])))
            nb_couples: int = math.floor((1 - durete) * (self.domain_size * self.domain_size))
            possible_couples: list[tuple[int, int]] = []

            # Définition des couples de valeurs possibles
            for i in range(self.domain_size):
                for j in range(self.domain_size):
                    possible_couples.append((i,j))
            
            # Tirage des couples de valeurs autorisés
            couples: list[tuple[int, int]] = []
            for i in range(nb_couples):
                couples.append(possible_couples.pop(random.randint(0, len(possible_couples) - 1)))
            
            # Assignation des couples de valeurs dans le tableau des contraintes
            couples.sort()
            self.constraints[first_var][second_var] = couples
        
        # self.print()
    
    def _is_coherent(self, values: list[int|None])-> bool:
        """Tests if the proposed values are coherent, meaning they break no constraint.

        Args:
            values (list[int|None]): List of proposed values for all variables, None meaning no value is proposed.

        Returns:
            bool: Indicate if the proposed values are coherent.
        """

        if len(values) != self.nb_variables:
            return False
        else:
            for i in range(self.nb_variables):
                for j in range(i+1, self.nb_variables):
                    if i != j and values[i] != None and values[j] != None:
                        constraint: list[tuple[int, int]]|None = self.constraints[i][j]
                        # print("(", i, j, ") :", constraint)
                        if constraint != None and (values[i], values[j]) not in self.constraints[i][j]:
                            # print("\t!! Values (", values[i], values[j], ") not in constraints")
                            return False
                        # else: print("\tValues (", values[i], values[j], ") in constraints")
            return True

    def _extend(self, candidate: list[int|None])-> list[int|None]|None:
        """Retourne candidate dans lequel la première instance de None est remplacée par la première valeur possible (0), 
        ou None si c'est impossible.

        Args:
            candidate (list[int | None]): La liste de valeurs à traiter.

        Returns:
            list[int|None]|None: La liste traitée, ou None si candidate ne contient aucun None.
        """
        candidate = candidate.copy()
        if not None in candidate:
            return None
        else:
            for i in range(len(candidate)):
                if candidate[i] == None:
                    candidate[i] = 0
                    return candidate
    
    def _next(self, candidate: list[int|None])-> list[int|None]|None:
        """Retourne candidate dans lequel la dernière variable ne valant pas None a été incrémentée, ou None si la fin du domaine a 
        été atteinte.

        Args:
            candidate (list[int | None]): La liste de valeurs à traiter.

        Returns:
            list[int|None]|None: La liste traitée, ou None si la fin du domaine a été atteinte.
        """
        candidate = candidate.copy()
        for i in range(len(candidate)-1, -1, -1):
            if candidate[i] != None:
                if candidate[i] == self.domain_size - 1:
                    return None
                else:
                    candidate[i] += 1
                    return candidate
     
    def print(self):
        print("\n####")
        print("Variables :\t", end="")
        for i in range(self.nb_variables):
            print(i, end="  ")
        print()
        print("Domain size :\t", self.domain_size)
        for i in range(self.nb_variables):
            for j in range(i+1, self.nb_variables):
                if self.constraints[i][j] != None:
                    print(i, " -- ", self.constraints[i][j], " -- ", j)
        print("####\n")


# csp = CSP(4, 3)
# csp.generate_constraints(0.5, 0.5)

# print(csp.test_values([0, 1, 2, 3]))
# print("Backtracking :")
# print(csp.backtracking())

# csp = CSP(4,3)
# csp.print()
# csp.generate_constraints(0.5, 0.5)
# print("Backtracking :", csp.backtracking())