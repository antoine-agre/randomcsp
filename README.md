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

Compare average execution time of the 3 algorithms over a number of generated CSPs.

For each CSP/algorithm pair, measure the average of ~5 executions to obtain a single data point. For each set of CSP parameters, generate ~5 CSPs and average to generate a single data point.

Variables to vary : CSP size (domain size, number of variables), constraints complexity (density, tightness).

- 1 plot per measure type (wall time, cpu time)
- 1 couple of plots per density/tightness couple
- On 1 plot (given measure type, density and tightness) : x is number of variables, y is time, with multiple bars for each x being domain size.

TODO : 
- measure by time backtracked and number of consistency checks
- fix forward checking
- log scale on y ?
- save data 
- change default parameter values for faster measures
- redo measure if csp has no solution (doesn't seem to happen ? or very rarely)


## build

Dans /randomscp :

`pyinstaller -F randomscp/__main__.py`

Génère un exécutable standalon.

> Penser à ajouter un `input()` ou autre pour empêcher la console de se fermer après exécution