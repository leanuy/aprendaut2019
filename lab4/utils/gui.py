### DEPENDENCIAS
### ------------------

import os
import sys

from .const import MenuOps

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
    print ("1. PCA a corpus Aquienvoto.uy tomando 2 dimensiones")
    print ("2. TBD")
    print ("0. Salir")

# Lee la opcion a elegir del menu principal
def printMenuOption():
    print ("")   
    print ("-> Elija una opción: ")
    op = int( input() )

    if op < 1 or op > 4:
        sys.exit()
    else:
        if op == 1:
            op = MenuOps.PCA
        elif op == 2:
            op = None

    return op
