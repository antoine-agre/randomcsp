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
        self.constraints: list[list[list[tuple[int, int]]|None]] = []

        for i in range(nb_variables):
            self.constraints.append([])
            for j in range(nb_variables):
                self.constraints[i].append(None)
    
    def generate_constraints(self, density: float, durete: float)-> None:
        """Génère des contraintes selon les paramètres de densité et de dureté.

        Args:
            density (float): Dans [0;1], proportion des couples de variables qui doivent posséder une contrainte.
            durete (float): Dans [0;1] ; pour toutes les contraintes, proportion des couples de valeurs possibles qui seront autorisées.
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
    
    def is_coherent(self, values: list[int|None])-> bool:
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
                        if constraint != None and (values[i], values[j]) not in self.constraints[i][j]:
                            return False
            return True

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