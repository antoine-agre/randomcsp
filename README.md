# Génération aléatoire et résolution de Problèmes de Satisfaction de Contraintes (CSP)

*Antoine AGRÉ - 5A ICy - INSA Hauts-de-France - Automne 2023*

## Table des matières

1. [Contexte](#contexte)
    1. [Sujet et objectifs](#sujet-et-objectifs)
    2. [Format du rendu](#format-du-rendu)
2. [Programme](#programme)
    1. [Modélisation du problème](#modélisation-du-problème)
    2. [Structure du programme](#structure-du-programme)
3. [Résultats](#résultats)
    1. [Mesures](#mesures)
    2. [Analyse](#analyse)

---

## Contexte

Ce programme a été réalisé dans le cadre du cours de **Programmation par Contraintes**, qui a surtout porté sur les Problèmes de Satisfaction de Contraintes (CSP) et les méthodes, algorithmes, heuristiques et langages utilisés pour les résoudre.

### Sujet et objectifs

Le sujet porte sur deux objectifs :

1. **Générer aléatoirement des CSP** selon 4 paramètres :
    - Le **nombre de variables** ;
    - La **taille des domaines** de ces variables ; 
    - La **densité du CSP** (la proportion des couples de variables qui possèdent une contrainte) ;
    - La **dureté des contraintes** du CSP (la proportion des couples de valeurs possibles qui sont autorisés pour chaque contrainte) ;
2. **Implémenter et appliquer 3 algorithmes** de recherche de solution de CSP :
    - Le **backtracking chronologique** "naïf" ;
    - Le **backjumping basé sur le graphe** (Graph-Based Backjumping) ;
    - Le **forward-checking**.

Aucun filtrage n'est utilisé. 

Pour simplifier leur exécution, les algorithmes s'arrêteront à la première solution trouvée, et leur but peut donc être considéré comme état de vérifier l'existence de solutions pour un CSP donné. 

Les assignations potentielles seront explorées dans le même ordre pour chaque algorithme, et ils devraient donc tous retourner la même solution si elle existe. 

### Format du rendu

c

## Programme

d

### Modélisation du problème

e

### Structure du programme

f

## Résultats

g

### Mesures

h

### Analyse

i




<br><br><br><br><br><br><br><br><br><br>
---

# Constraint Satisfaction Problem (CSP) random generation and solving

$V = \{V_1, V_2, \dots, V_n\}$ : variables

$D = \{D_1, D_2, \dots, D_n\}$ : domaines

$C = \{C_1, C_2, \dots, C_m\}$ : contraintes

## Backtracking

## Backjumping

- Structure de donnée représentant le graphe associé au CSP
    - Chaque variable à des ancètres

## Timer

### Goal

Compare **average execution time**, **number of backtracks** and **number of consistency checks** of the 3 algorithms over a number of generated CSPs.

For each CSP/algorithm pair, measure the average of ~5 executions to obtain a single data point for each measure. For each set of CSP parameters, generate ~5 CSPs and average to generate a single data point.

Variables to vary : CSP size (domain size, number of variables), constraints complexity (density, tightness).

- For each series, we choose one parameter to vary while the others stay constant.
- For every measure, we make one plot for each measure type (cpu time, backtracks, consistency checks)
- In every plot, we compare the results of the different algorithms

| **Variable parameter** | **CPU Time** | **Number of backtracks** | **Number of consistency checks** |
|---|---|---|---|
| **Domain size** |  |  |  |
| **Number of variables** |  |  |  |
| **Density** |  |  |  |
| **Tightness** |  |  |  |

- ~~1 plot per measure type (cpu time, backtracks, consistency checks)~~
- ~~1 group of those plots per density/tightness couple~~
- ~~On 1 plot (given measure type, density and tightness) : x is number of variables, y is time, with multiple bars for each x being domain size.~~

TODO : 
- measure by time backtracked and number of consistency checks
- ~~fix forward checking~~
- log scale on y ?
- save data 
- change default parameter values for faster measures
- redo measure if csp has no solution (doesn't seem to happen ? or very rarely)
- cut off extreme times from measures ?


## build

Dans /randomscp :

`pyinstaller -F randomcsp/__main__.py`

Génère un exécutable standalone.

> Penser à ajouter un `input()` ou autre pour empêcher la console de se fermer après exécution

`tests.exe` : full tests
`smaller_tests.exe` : only 3 first values for each parameter