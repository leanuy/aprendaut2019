### DEPENDENCIAS
### ------------------

import os
import sys

from .const import MenuOps, PCAOps, PCAnalysis, PCAIntermediates, KmeansAnalysis, KmeansEvaluations, CandidateDivision

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
    print ("#       MENÚ - Laboratorio 4 (Análisis de datos - PCA, K-Means)        #")
    print ("#                                                                      #")
    print ("########################################################################")
    print ("")
    print ("1. Reducir dimensiones (PCA)")
    print ("2. Generar clusters (K-Means)")
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
            op = MenuOps.PCA
        elif op == 2:
            op = MenuOps.KMEANS

    return op

# Lee la opción a elegir de como implementar PCA
def printPCAOptions():
    print ("")
    print ("-> Elija un método de reducción PCA: ")
    print ("-> DEFAULT: 1")
    print ("1. Matriz de Covarianza")
    print ("2. Descomposición SVD")

    try:
        op = int( input() )    
        if op < 1 or op > 2:
            op = PCAOps.COVARIANZA
        else:
            if op == 1:
                op = PCAOps.COVARIANZA
            elif op == 2:
                op = PCAOps.SVD
        return op
    except:
        return PCAOps.COVARIANZA

# Lee la opción a elegir de que datos mostrar de PCA
def printPCAnalysis():
    print ("")
    print ("-> Elija que datos graficar: ")
    print ("-> DEFAULT: 0")
    print ("1. Graficar conjunto de datos")
    print ("2. Graficar conjunto de datos diviendo por partido")
    print ("3. Graficar conjunto de datos para cada partido")
    print ("0. Ninguno")
    
    try:
        op = int( input() )
        if op < 0 or op > 3:
            op = PCAnalysis.NONE
        else:
            if op == 0:
                op = PCAnalysis.NONE
            elif op == 1:
                op = PCAnalysis.GENERAL
            elif op == 2:
                op = PCAnalysis.ALL_PARTY
            elif op == 3:
                op = PCAnalysis.EACH_PARTY
        return op
    except:
        return PCAnalysis.NONE

# Lee la opción a elegir de que datos intermedios mostrar de PCA
def printPCAIntermediate(pca_election):
    if pca_election != PCAOps.COVARIANZA:
        return PCAIntermediates.NONE

    print ("")
    print ("-> Elija que resultados intermedios mostrar: ")
    print ("-> DEFAULT: 0")
    print ("1. Matriz de Covarianza")
    print ("2. Valores Propios")
    print ("3. Ratio de Varianza")
    print ("0. Ninguno")
    
    try:
        op = int( input() )
        if op < 0 or op > 3:
            op = PCAIntermediates.NONE
        else:
            if op == 0:
                op = PCAIntermediates.NONE
            elif op == 1:
                op = PCAIntermediates.COV_MATRIX
            elif op == 2:
                op = PCAIntermediates.EIGEN_VALUES
            elif op == 3:
                op = PCAIntermediates.VARIANCE_RATIO
        return op
    except:
        return PCAIntermediates.NONE

# Imprime las opciones para K y lee la opción elegida
def printModelK(modelType):
    if modelType != MenuOps.KMEANS:
        return 5
    else:
        print ("")
        print ("-> Elija cantidad de clusters para generar: ")
        print ("-> DEFAULT: 5")
        try:
            evaluationK = int( input() )
            return evaluationK
        except:
            return 5

# Imprime opciones para la cantidad de veces que se desee ejeutar K-Means
def printItersK(modelType):
    if modelType != MenuOps.KMEANS:
        return 1
    else:
        print ("")
        print ("-> Elija cantidad de K-Means para ejecutar: ")
        print ("-> DEFAULT: 1")
        try:
            evaluationK = int( input() )
            return evaluationK
        except:
            return 1

# Lee la opción a elegir de que datos mostrar de KMeans
def printKmeansAnalysis():
    print ("")
    print ("-> Elija que datos graficar: ")
    print ("-> DEFAULT: 0")
    print ("1. Graficar candidatos en cada cluster")
    print ("2. Graficar partidos en cada cluster")
    print ("0. Ninguno")
    
    try:
        op = int( input() )
        if op < 0 or op > 2:
            op = KmeansAnalysis.NONE
        else:
            if op == 0:
                op = KmeansAnalysis.NONE
            elif op == 1:
                op = KmeansAnalysis.GENERAL
            elif op == 2:
                op = KmeansAnalysis.PARTIES
        return op
    except:
        return KmeansAnalysis.NONE

# Lee la opción a elegir de que evaluaciones realizar a los clusters de Kmeans
def printKmeansEvaluations(k):
    showARI = k == 3 or k == 5 or k == 11 
    print ("")
    print ("-> Elija que evaluación calcular: ")
    print ("-> DEFAULT: 0")
    print ("1. Coeficiente Silhouette")
    if showARI:
        print ("2. Adjusted Random Index")
    print ("0. Ninguno")
    
    try:
        op = int( input() )
        if op < 0 or op > 2:
            op = KmeansEvaluations.NONE
        else:
            if op == 0:
                op = KmeansEvaluations.NONE
            elif op == 1:
                op = KmeansEvaluations.SILHOUETTE
            elif op == 2 and showARI:
                op = KmeansEvaluations.ARI
            else:
                op = KmeansEvaluations.NONE
        return op
    except:
        return KmeansEvaluations.NONE

# Lee la opción a elegir de que división utilizar para los candidatos
def printCandidateDivision(analisis):
    if analisis != PCAnalysis.ALL_PARTY and analisis != KmeansAnalysis.PARTIES:
        return CandidateDivision.PARTIES

    print ("")
    print ("-> Elija como dividir a los candidatos: ")
    print ("-> DEFAULT: 1")
    print ("1. Por Partido (FA, PN, PC, etc.)")
    print ("2. Por Espectro General (Izquierda, Centro, Derecha)")
    print ("3. Por Espectro de Nolan (Progresismo, Totalitarismo, Conservadurismo, Liberalismo, Centro)")
    
    try:
        op = int( input() )
        if op < 1 or op > 3:
            op = CandidateDivision.PARTIES
        else:
            if op == 1:
                op = CandidateDivision.PARTIES
            elif op == 2:
                op = CandidateDivision.SPECTRUM
            elif op == 3:
                op = CandidateDivision.NOLAN
        return op
    except:
        return CandidateDivision.PARTIES