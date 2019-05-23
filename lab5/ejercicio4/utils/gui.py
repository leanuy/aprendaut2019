### DEPENDENCIAS
### ------------------

import os
import sys

from .const import MenuOps, SolverOps, PenaltyOps, CandidateDivision

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
def printMenu(classifiers):
    printClear()
    print ("##########################################################")
    print ("#                                                        #")
    print ("#    MENÚ - Laboratorio 5 (Regresión Logística - PCA)    #")
    print ("#                                                        #")
    print ("##########################################################")
    print ("")
    printClassifiers(classifiers)
    print ("1. Entrenar")
    print ("2. Evaluar")
    print ("3. Graficar")
    print ("0. Salir")

# Lee la opción a elegir del menu principal
def printMenuOption():
    print ("")   
    print ("-> Elija una opción: ")
    op = int( input() )

    if op < 1 or op > 3:
        sys.exit()
    else:
        if op == 1:
            op = MenuOps.TRAIN
        elif op == 2:
            op = MenuOps.EVALUATE
        elif op == 3:
            op = MenuOps.PLOT

    return op

# Imprime la lista de clasificadores entrenados
def printClassifiers(classifiers):
    print ("Clasificadores actuales:")
    index = 1
    for c in classifiers:
        print("")
        print("-> ", end="")
        print(str(index), end="")
        print(" - ", end="")
        print("Clasificadores por Regresión Logística (candidato/partido)")

        print("   Dimensionalidad: ", end="")
        if c.options['pca_dimension'] == 0:
            print('26 (Sin PCA)')
        else:
            print(c.options['pca_dimension'])

        print("   Algoritmo: ", end="")
        print(c.options['solver'])

        print("   Penalización: ", end="")
        print(c.options['penalty'])

        print("   Iteraciones: ", end="")
        print(c.options['max_iter'])

        print("   Regularización: ", end="")
        print(c.options['regulation_strength'])

        index = index + 1
        
    print ("")

# Lee la cantidad de dimensiones a reducir con PCA (0 si no se quiere aplicar PCA)
def printPCADimension():
    print ("")
    print ("-> Ingrese cantidad de dimensiones a obtener con PCA:")
    print ("-> DEFAULT: 0 (No se aplica PCA)")
    print ("-> (Máximo 25)")
    try:
        dimensions = int( input() )
        return dimensions
    except:
        return 0

# Lee la opción a elegir de que algoritmo implementar
def printSolverOptions():
    print ("")
    print ("-> Elija un algoritmo para implementar la regresión: ")
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
                op = SolverOps.LIBLINEAR
            elif op == 2:
                op = SolverOps.LBFGS
            elif op == 3:
                op = SolverOps.SAG
            elif op == 4:
                op = SolverOps.SAGA
            elif op == 5:
                op = SolverOps.NEWTON_CG
        return op
    except:
        return SolverOps.LIBLINEAR

# Lee la opción a elegir de que penalización usar en la regularización
def printPenaltyOptions(solver_election):
    print ("")
    print ("-> Elija una estrategia de penalización para la regularización: ")
    print ("-> DEFAULT: 1")

    if solver_election == SolverOps.LBFGS or solver_election == SolverOps.SAG or solver_election == SolverOps.NEWTON_CG:
        print ("1. L2 (Regresión Ridge). Única opción para solver {}".format(solver_election))        


    elif solver_election == SolverOps.SAGA:
        print ("1. L2 (Regresión Ridge)")
        print ("2. L1 (Regresión Lasso)")
        print ("0. Ninguna")

    elif solver_election == SolverOps.LIBLINEAR:
        print ("1. L2 (Regresión Ridge)")
        print ("2. L1 (Regresión Lasso)")

    try:
        op = int( input() )
        if op < 0 or op > 2:
            if solver_election == SolverOps.LIBLINEAR:
                op = PenaltyOps.L2
            else:
                op = PenaltyOps.NONE
        else:
            if op == 0:
                op = PenaltyOps.NONE
            elif op == 1:
                op = PenaltyOps.L2
            elif op == 2:
                op = PenaltyOps.L1
        return op
    except:
        if solver_election == SolverOps.LIBLINEAR or solver_election == SolverOps.LBFGS or \
                solver_election == SolverOps.SAG or solver_election == SolverOps.NEWTON_CG:
            return PenaltyOps.L2
        else:
            return PenaltyOps.NONE

# Lee el máximo de iteraciones a hacer en caso de no converger
def printIterations():
    print ("")
    print ("-> Ingrese cantidad maxima de iteraciones en caso de no converger: ")
    print ("-> DEFAULT: 1000")
    try:
        max_iter = int( input() )
        return max_iter
    except:
        return 1000

# Lee parámetro de regularización
def printRegulationStrength():
    print ("")
    print ("-> Ingrese (inverso de) parámetro de regularización: ")
    print ("-> DEFAULT: 1.0")
    try:
        C = float( input() )
        return C
    except:
        return 1.0

# Lee la cantidad de particiones para la validación cruzada
def printCrossK():
    print ("")
    print ("-> Ingrese cantidad de particiones para evaluación cruzada: ")
    print ("-> DEFAULT: 0 (Validación normal)")
    try:
        k = int( input() )
        return k
    except:
        return 0

# Imprime los datos de la evaluación 'evaluation'
def printEvaluation(evaluation, k):
    # Imprimir normal
    if k == 0:
        print("---------- Clasificación según candidatos ----------")
        print("-> Accuracy: ", end="")
        print(evaluation['accuracy_candidates'])
    
        print("-> Matriz de Confusión: ")
        print()
        print(evaluation['confusion_matrix_candidates'])
        print()

        print("-> Métricas: ")
        print()
        print(evaluation['report_candidates'])
        print()
        print("---------- Clasificación según partidos ----------")
        print("-> Accuracy: ", end="")
        print(evaluation['accuracy_parties'])
    
        print("-> Matriz de Confusión: ")
        print()
        print(evaluation['confusion_matrix_parties'])
        print()

        print("-> Métricas: ")
        print()
        print(evaluation['report_parties'])
        print()
    else:
        print("---------- Clasificación según candidatos ----------")
        print("-> Accuracy cross validation con k = {}: ".format(k), end="")
        print(evaluation['cv_accuracy_candidates'])
    
        print("-> Matriz de Confusión cross validation con k = {}: ".format(k))
        print()
        print(evaluation['cv_confusion_matrix_candidates'])
        print()

        print("-> Métricas cross validation con k = {}: ".format(k))
        print()
        print(evaluation['cv_report_candidates'])
        print()
        print("---------- Clasificación según partidos ----------")
        print("-> Accuracy cross validation con k = {}: ".format(k), end="")
        print(evaluation['cv_accuracy_parties'])
    
        print("-> Matriz de Confusión cross validation con k = {}: ".format(k))
        print()
        print(evaluation['cv_confusion_matrix_parties'])
        print()

        print("-> Métricas cross validation con k = {}: ".format(k))
        print()
        print(evaluation['cv_report_parties'])
        print()

    if evaluation['explained_variance_ratio'] is not None:
        print("-> Proporción de varianza explicada: ")
        print()
        print(evaluation['explained_variance_ratio'])
        print()