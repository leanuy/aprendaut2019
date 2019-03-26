### DEPENDENCIAS
### ------------------

import os
import sys

from .const import MenuOps, ModelOps, ContinuousOps, EvaluationOps, IRIS_DATASET, COVERTYPE_DATASET

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
    print ("4. Mostrar")
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
            op = MenuOps.TRAIN
        elif op == 2:
            op = MenuOps.CLASSIFY
        elif op == 3:
            op = MenuOps.EVALUATE
        elif op == 4:
            op = MenuOps.SHOW

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

# Imprime las opciones de conjunto de datos y lee la opción elegida
def printDataset():
    print ("")
    print ("-> Elija un conjunto de datos como fuente del entrenamiento: ")
    print ("-> DEFAULT: 1")
    print ("1. Iris")
    print ("2. CoverType")

    try:
        dataset = int( input() )
        if dataset == 2:
            return COVERTYPE_DATASET
        else:
            return IRIS_DATASET

    except:
        return IRIS_DATASET

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
                modelName = "Árbol"
            elif modelType == 2:
                modelType = ModelOps.DECISION_FOREST
                modelName = "Bosque"

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

# Imprime las estrategias de evaluación y lee la opción elegida
def printEvaluationMode():
    print ("")
    print ("-> Elija un algoritmo de evaluación: ")
    print ("-> DEFAULT: 1")
    print ("1. Validación normal")
    print ("2. Validación cruzada")

    try:
        evaluation = int( input() )
        if evaluation == 2:
            return EvaluationOps.CROSS
        else:
            return EvaluationOps.NORMAL

    except:
        return EvaluationOps.NORMAL

# Imprime los datos de entrenamiento de un clasificador
def printEvaluation(classifier, eval, accuracy, confusionMatrix):

    print()
    print("-> Modelo Entrenado - ", end="")
    print(classifier['name'])
    print("--> Estrategia de atributos continuos: ", end="")
    print(classifier['continuous'])

    print()

    print("-> Evaluación normal (80/20)")
    print("--> Accuracy: ", end="")
    print(accuracy)
    print("--> Confusion Matrix: ")
    print()
    printConfusionMatrix(confusionMatrix, classifier['results'])

    for result in eval:
        print()
        print("--> Evaluación para ", end="")
        print(result, end=": ")
        print()
        (precision, recall, Fmeasure) = eval[result]
        print("---> Precision: ", end="")
        print(precision)
        print("---> Recall: ", end="")
        print(recall)        
        print("---> F-Measure: ", end="")
        print(Fmeasure)
        
    print()

# Imprime los datos de entrenamiento de un clasificador
def printConfusionMatrix(confusionMatrix, results):

    maxWordLength = 0
    for result in results:
        length = len(result)
        if length > maxWordLength:
            maxWordLength = length

    print(' ' * maxWordLength, end=" ")

    for result in results:
        print(result, end=" ")

    print()
    print()

    for i in range(0, len(results)):

        print(results[i], end=" ")
        if len(results[i]) < maxWordLength:
            print(' ' * (maxWordLength - len(results[i])), end="")

        for j in range(0, len(results)):
            print(' ' * (len(results[j]) // 2), end="")
            print(confusionMatrix[i][j], end=" ")
            print(' ' * (len(results[j]) // 2), end="")

        print()
        print()