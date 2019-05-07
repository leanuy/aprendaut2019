### DEPENDENCIAS
### ------------------

import os
import sys

from .const import MenuOps, PCAOps, PCAnalysis, PCAIntermediates

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
    print ("0. Ninguno")
    
    try:
        op = int( input() )
        if op < 0 or op > 2:
            op = PCAIntermediates.NONE
        else:
            if op == 0:
                op = PCAIntermediates.NONE
            elif op == 1:
                op = PCAIntermediates.COV_MATRIX
            elif op == 2:
                op = PCAIntermediates.EIGEN_VALUES
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