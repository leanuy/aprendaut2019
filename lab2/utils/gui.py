### DEPENDENCIAS
### ------------------

import os
import sys

from .const import MenuOps, ModelOps, ContinuousOps

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
    print ("############################################################")
    print ("#                                                          #")
    print ("#        MENÚ - Laboratorio 2 (Árboles de Decisión)        #")
    print ("#                                                          #")
    print ("############################################################")
    print ("")
    printClassifiers(classifiers)
    print ("1. Entrenar")
    print ("2. Clasificar")
    print ("3. Evaluar")
    print ("0. Salir")

# Lee la opcion a elegir del menu principal
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
            op = MenuOps.CLASSIFY
        elif op == 3:
            op = MenuOps.EVALUATE

    return op

# Imprime la lista de clasificadores entrenados
def printClassifiers(classifiers):
    print ("Clasificadores actuales:")
    index = 1
    for c in classifiers:
        print("-> ", end="")
        print(str(index), end="")
        print(" - ", end="")
        print("Clasificador ", end="")
        print(c['name'])
        index = index + 1
    print ("")

# Imprime las opciones de tipo de modelo y lee la opción elegida
def printModelType():
    print ("")
    print ("-> Elija un tipo de modelo para entrenar: ")
    print ("-> DEFAULT: 1")
    print ("1. Árbol")
    print ("2. Bosque")

    try:
        modelType = int( input() )

        if modelType < 1 or modelType > 2:
            return (ModelOps.DECISION_TREE, "Árbol")
        else:
            if modelType == 1:
                modelType = ModelOps.DECISION_TREE
                modelName = "Random"
            elif modelType == 2:
                modelType = ModelOps.DECISION_FOREST
                modelName = "Si Mismo"

        return (modelType, modelName)

    except:
        return (ModelOps.DECISION_TREE, "Árbol")

# Imprime las estrategias para tratar atributos continuos y lee la opción elegida
def printContinuousStrategy():
    print ("")
    print ("-> Elija una estrategia para tratar atributos continuos: ")
    print ("-> DEFAULT: 1")
    print ("1. Partir en intervalos fijos, por defecto 3")
    print ("2. Partir en intervalos variables, según resultado")

    try:
        continuousStrategy = int( input() )

        if continuousStrategy < 1 or continuousStrategy > 2:
            return ContinuousOps.FIXED
        else:
            if continuousStrategy == 1:
                continuousStrategy = ContinuousOps.FIXED
            elif continuousStrategy == 2:
                continuousStrategy = ContinuousOps.VARIABLE

        return continuousStrategy

    except:
        return ContinuousOps.FIXED
    
# Imprime los datos de entrenamiento de un clasificador
def printTrainedClassifier(classifier):

    print("-> Modelo Entrenado - ", end="")
    print(classifier['name'])

    print("--> Tiempo de entrenamiento: ", end="")
    print(classifier['time'], end=" ")
    print("segundos")

    print("--> Estrategia de atributos continuos: ", end="")
    print(classifier['continuous'])

    print()