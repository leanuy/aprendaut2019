### DEPENDENCIAS
### ------------------

import os
import sys
import operator

from .const import MenuOps, PlotOps, SolverOps, PenaltyOps, CandidateDivision

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
    print ("1. Entrenar clasificador")
    print ("2. Evaluar clasificador")
    print ("3. Graficar datos de clasificador")
    print ("4. Buscar mejor clasificador")
    print ("0. Salir")

# Lee la opción a elegir del menu principal
def printMenuOption():
    print ("")   
    print ("-> Elija una opción: ")
    op = int( input() )

    if op < 1 or op > 4:
        sys.exit()
    else:
        if op == 1:
            op = MenuOps.TRAIN
        elif op == 2:
            op = MenuOps.EVALUATE
        elif op == 3:
            op = MenuOps.PLOT
        elif op == 4:
            op = MenuOps.SEARCH

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

### METODOS AUXILIARES - TRAIN
### ----------------------------

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

    elif solver_election == SolverOps.LIBLINEAR or solver_election == SolverOps.SAGA:
        print ("1. L2 (Regresión Ridge)")
        print ("2. L1 (Regresión Lasso)")

    try:
        op = int( input() )
        if op < 1 or op > 2:
            op = PenaltyOps.L2
        else:
            if op == 1:
                op = PenaltyOps.L2
            elif op == 2:
                op = PenaltyOps.L1
        return op
    except:
        return PenaltyOps.L2

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

### METODOS AUXILIARES - EVALUATE
### ----------------------------

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

    print()

    # Imprimir normal
    if k == 0:
        
        print("-> EVALUACIÓN NORMAL")
        print()  
        print("---------- Clasificación según candidatos ----------")
        print()
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
        print()
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
        print(f"-> EVALUACIÓN CRUZADA (k = {k})")
        print() 
        print("---------- Clasificación según candidatos ----------")
        print()
        print("-> Accuracy: ", end="")
        print(evaluation['cv_accuracy_candidates'])
    
        print("-> Matriz de Confusión: ")
        print()
        print(evaluation['cv_confusion_matrix_candidates'])
        print()

        print("-> Métricas: ")
        print()
        print(evaluation['cv_report_candidates'])
        print()
        print("---------- Clasificación según partidos ----------")
        print()
        print("-> Accuracy: ", end="")
        print(evaluation['cv_accuracy_parties'])
    
        print("-> Matriz de Confusión: ")
        print()
        print(evaluation['cv_confusion_matrix_parties'])
        print()

        print("-> Métricas: ")
        print()
        print(evaluation['cv_report_parties'])
        print()

    if evaluation['explained_variance_ratio'] is not None:
        print("-> Proporción de varianza explicada: ")
        print()
        print(evaluation['explained_variance_ratio'])
        print()

# Lee la cantidad de particiones para la validación cruzada
def printCheckPCA():
    print ("")
    print ("-> Desea buscar mejor dimensión de PCA? (y/n): ")
    print ("-> DEFAULT: n")
    try:
        pca = input()
        return pca == 'y'
    except:
        return False

### METODOS AUXILIARES - PLOT
### ----------------------------

# Lee la opción a elegir del menu de graficas
def printPlotOption():
    print ("")   
    print ("-> Elija una opción para graficar: ")
    print ("-> DEFAULT: 1")
    print ("1. Graficar datos del corpus")
    print ("2. Graficar datos de evaluación de un modelo")
    print ("3. Graficar datos de comparación de todos los modelos")
    
    try:
        op = int( input() )
        if op < 1 or op > 3:
            return PlotOps.CORPUS
        else:
            if op == 1:
                op = PlotOps.CORPUS
            elif op == 2:
                op = PlotOps.SINGLE
            elif op == 3:
                op = PlotOps.ALL
            return op
    except:
        return PlotOps.CORPUS

### METODOS AUXILIARES - SEARCH
### ----------------------------

# Imprime los datos de entrenamiento de un clasificador durante la busqueda
def printClassifierTraining(index, options):

        print("")
        print("Iniciando entrenamiento")
        
        print("-> ", end="")
        print(str(index), end="")
        print(" - ", end="")

        print("Clasificadores por Regresión Logística (candidato/partido)")
        print("   Algoritmo: ", end="")
        print(options['solver'])
        print("   Penalización: ", end="")
        print(options['penalty'])
        print("   Iteraciones: ", end="")
        print(options['max_iter'])
        print("   Regularización: ", end="")
        print(options['regulation_strength'])

        if options['pca_dimension'] != 0:
            print("   Dimensionalidad: ", end="")
            print(options['pca_dimension'])

# Imprime los datos de la evaluación de un clasificador durante la busqueda
def printClassifierEvaluation(accuracy_candidates, accuracy_parties):
    print(f'-> Accuracy (Candidatos): {accuracy_candidates}')
    print(f'-> Accuracy (Partidos): {accuracy_parties}')

# Imprime los datos del mejor clasificador y su accuracy
def printBestClassifiers(candidate_classificators, party_classificators):

    candidate_classificators = sorted(candidate_classificators, key=operator.itemgetter(0), reverse=True)
    party_classificators = sorted(party_classificators, key=operator.itemgetter(0), reverse=True)

    accuracy_candidates, model_candidates = candidate_classificators[0]
    accuracy_parties, model_parties = party_classificators[0]

    print()
    printClassifierData(model_candidates.options, 'candidato')
    print(f'-> Accuracy: {accuracy_candidates}')
    print()
    printClassifierData(model_parties.options, 'partido')
    print(f'-> Accuracy: {accuracy_parties}')
    print()

# Imprime los datos de un clasificador
def printClassifierData(options, title):
        print(f"-> Clasificador por {title} (Regresión Logística)")
        print("   Algoritmo: ", end="")
        print(options['solver'])
        print("   Penalización: ", end="")
        print(options['penalty'])
        print("   Iteraciones: ", end="")
        print(options['max_iter'])
        print("   Regularización: ", end="")
        print(options['regulation_strength'])

        if options['pca_dimension'] != 0:
            print("   Dimensionalidad: ", end="")
            print(options['pca_dimension'])
