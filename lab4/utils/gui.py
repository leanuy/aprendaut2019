### DEPENDENCIAS
### ------------------

import os
import sys

from .const import MenuOps, PCAOps, PCAnalysis

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
    print ("#    MENÚ - Laboratorio 4 (PCA - K-Means - Deteccion de anomalias )    #")
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
    print ("1. Usando matriz de covarianza")
    print ("2. Usando SVD")
    op = int( input() )

    if op < 1 or op > 2:
        op = PCAOps.COVARIANZA
    else:
        if op == 1:
            op = PCAOps.COVARIANZA
        elif op == 2:
            op = PCAOps.SVD

    return op

# Lee la opción a elegir de como implementar PCA
def printPCAnalysis():
    print ("")
    print ("-> Elija un método de reducción PCA: ")
    print ("-> DEFAULT: 1")
    print ("1. Graficar conjunto de datos")
    print ("2. Graficar conjunto de datos diviendo por partido")
    print ("3. Graficar conjunto de datos para cada partido")
    op = int( input() )

    if op < 1 or op > 3:
        op = PCAnalysis.GENERAL
    else:
        if op == 1:
            op = PCAnalysis.GENERAL
        elif op == 2:
            op = PCAnalysis.ALL_PARTY
        elif op == 3:
            op = PCAnalysis.EACH_PARTY

    return op
