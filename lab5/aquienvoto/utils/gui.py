### DEPENDENCIAS
### ------------------

import os
import sys

from .const import MenuOps, SOLVEROps, PENALTYOps, PCAIntermediates, KmeansAnalysis, KmeansEvaluations, CandidateDivision

### METODOS AUXILIARES - MENU
### -------------------------

# Limpia la consola
def printClear():
    if os.name == 'nt':
        clear = lambda : os.system('cls')
        clear()
    else:
        clear = lambda : os.system('clear')
        clear()

# Imprime el menu principal
def printMenu():
    printClear()
    print ("########################################################################")
    print ("#                                                                      #")
    print ("#    MENÚ - Laboratorio 5 (Ejercicio 4 - Regresion Logistica - PCA)    #")
    print ("#                                                                      #")
    print ("########################################################################")
    print ("")
    print ("1. Aplicar Logistic Regression a dataset aquienvoto.uy")
    print ("2. PCA Editar opcion!!!")
    print ("0. Salir")

# Lee la opción a elegir del menu principal
def printMenuOption():
    print ("")   
    print ("-> Elija una opción: ")
    op = int( input() )

    if op < 1 or op > 2:
        sys.exit()
    else:
        if op == 1:
            op = MenuOps.LOGISTIC_REGRESSION
        elif op == 2:
            op = MenuOps.PCA

    return op

# Lee la opción a elegir de como implementar Logistic Regression
def printSOLVEROptions():
    print ("")
    print ("-> Elija un valor para solver: ")
    print ("-> DEFAULT: 1")
    print ("1. liblinear")
    print ("2. lbfgs")
    print ("3. sag")
    print ("4. saga")
    print ("5. newton-cg")

    try:
        op = int( input() )    
        if op < 1 or op > 5:
            op = SOLVEROps.LIBLINEAR
        else:
            if op == 1:
                op = SOLVEROps.LIBLINEAR
            elif op == 2:
                op = SOLVEROps.LBFGS
            elif op == 3:
                op = SOLVEROps.SAG
            elif op == 4:
                op = SOLVEROps.SAGA
            elif op == 5:
                op = SOLVEROps.NEWTON_CG
        return op
    except:
        return SOLVEROps.LIBLINEAR

# Lee la opción a elegir de que Penalty usar
def printPENALTYOptions(solver_election):
    
    if solver_election == SOLVEROps.LBFGS or solver_election == SOLVEROps.SAG or solver_election == SOLVEROps.NEWTON_CG:
        print ("")
        print ("-> Elija un penalty: ")
        print ("-> DEFAULT: 0")
        print ("0. None")
        print ("1. l2")
    elif solver_election == SOLVEROps.SAGA:
        print ("")
        print ("-> Elija un penalty: ")
        print ("-> DEFAULT: 0")
        print ("0. None")
        print ("1. l2")
        print ("2. l1")
        print ("3. elasticnet")
    elif solver_election == SOLVEROps.LIBLINEAR:
        print ("")
        print ("-> Elija un penalty: ")
        print ("-> DEFAULT: 1")
        print ("1. l2")
        print ("2. l1")

    try:
        op = int( input() )
        if op < 0 or (op > 2 and solver_election != SOLVEROps.SAGA):
            if solver_election == SOLVEROps.LIBLINEAR:
                op = PENALTYOps.L2
            else:
                op = PENALTYOps.NONE
        else:
            if op == 0:
                op = PENALTYOps.NONE
            elif op == 1:
                op = PENALTYOps.L2
            elif op == 2:
                op = PENALTYOps.L1
            elif solver_election == SOLVEROps.SAGA and op == 3:
                op = PENALTYOps.ELASTICNET
        return op
    except:
        if solver_election == SOLVEROps.LIBLINEAR:
            return PENALTYOps.L2
        else:
            return PENALTYOps.NONE

# Eleecion de max_iter
def printMaxIterations():
    print ("")
    print ("-> Elija cantidad maxima de iteraciones: ")
    print ("-> DEFAULT: 1000")
    try:
        max_iter = int( input() )
        return max_iter
    except:
        return 1000

# Imprime para elegir C regulation strength
def printRegulationStrength():
    print ("")
    print ("-> Ingrese valor para inverso de regulation strength: ")
    print ("-> DEFAULT: 1.0")
    try:
        C = int( input() )
        return C
    except:
        return 1.0

