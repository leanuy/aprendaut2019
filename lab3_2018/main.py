# Dependencias
# --------------------------------------------------------------------------------
import sys
import os
import pdb
import pandas as pd
from scipy.io import arff
import time

from preprocessor import get_dataset
from model import Model, ModelType
from evaluate import normal_validation, cross_validation

# Métodos auxiliares
# --------------------------------------------------------------------------------

def get_example(text, attributes):

    values = text.split(",")
    example = {}
    i = 0

    for att in attributes:
        example[att] = values[i]
        i = i + 1

    return example
def get_attributes(text):
    if text == '':
        return []
    else:
        return text.split(",")

def printClear():

    if os.name == 'nt':
        clear = lambda : os.system('cls')
        clear()
    else:
        clear = lambda : os.system('clear')
        clear()
def printMenu(classifiers):

    printClear()
    print ("#######################")
    print ("#        MENÚ         #")
    print ("#######################")
    print ("")
    printClassifiers(classifiers)
    print ("1. Entrenar")
    print ("2. Clasificar")
    print ("3. Evaluar")
    print ("0. Salir")
    print ("")
def printClassifiers(classifiers):

    continuousExplanationDT = [ "Ninguno", "3 Intervalos Fijos", "Intervalos variables" ]
    missingExplanationDT = [ "Ninguno", "Valor más probable", "Probabilidad por rama" ]

    continuousExplanationNB = [ "Ninguno", "Distribución Gaussiana", "Intervalos variables" ]
    missingExplanationNB = [ "Ninguno",  "M-estimador", "Ignorar" ]

    missingExplanationKNN = [ "Ninguno", "Valor más probable", "Ignorar" ]
    normExplanationKNN = [ "", "Norma Euclídea", "Norma min-max", "Z-score" ]

    if classifiers == []:
        return
    else:
        print ("Clasificadores actuales:")
        index = 0
        for c in classifiers:
            print("-> ", end="")
            print(str(index), end="")
            print(" - ", end="")
            print(c['name'], end="")
            print(" clasificador")

            if c['type'] == ModelType.DECISION_TREE:
                print("   Estrategia continua: ", end="")
                print(continuousExplanationDT[c['continuous']])
                print("   Estrategia faltante: ", end="")
                print(missingExplanationDT[c['missing']])

            elif c['type'] == ModelType.NAIVE_BAYES:
                print("   Estrategia continua: ", end="")
                print(continuousExplanationNB[c['continuous']])
                print("   Estrategia faltante: ", end="")
                print(missingExplanationNB[c['missing']])

            elif c['type'] == ModelType.KNN:
                print("   K-nearest: ", end="")
                print(c['k'])
                print("   Estrategia continua: ", end="")
                print(missingExplanationKNN[c['missing']])
                print("   Estrategia de normalización: ", end="")
                print(normExplanationKNN[c['norm']])

            print("")
            index = index + 1

def printModelType():
    print ("")
    print ("-> Elija un modelo para entrenar: ")
    print ("1. Decision tree")
    print ("2. Naive bayes")
    print ("3. K-nearest neighbors")
    modelType = int( input() )
    modelName = ''

    if modelType < 1 or modelType > 3:
        print("-> El primer argumento debe ser 1, 2 o 3.")
        sys.exit()
    else:
        if modelType == 1:
            modelType = ModelType.DECISION_TREE
            modelName = "Decision Tree"
        elif modelType == 2:
            modelType = ModelType.NAIVE_BAYES
            modelName = "Naive Bayes"
        elif modelType == 3:
            modelType = ModelType.KNN
            modelName = "K-Nearest Neighbors"

    return (modelType, modelName)
def printK(modelType):

    if modelType != ModelType.KNN:
        return 3
    else:
        print ("")
        print ("-> Elija un número k para KNN: ")
        k = int( input() )
        return k
def printM(modelType, missing):

    if modelType != ModelType.NAIVE_BAYES:
        return 0
    else:
        if missing != 1:
            return 0
        else:
            print ("")
            print ("-> Elija un número m para el m-estimador: ")
            k = int( input() )
            return k
def printContinuous(modelType):

    if modelType == ModelType.KNN:
        return 0
    else:
        print ("")
        print ("-> Elija una opción para valores continuos: ")

        if modelType == ModelType.DECISION_TREE:
            print ("1. 3 intervalos fijos, basados en dividir el datset entre 3")
            print ("2. Intervalos variables, basados en orden y clasificación")

        elif modelType == ModelType.NAIVE_BAYES:
            print ("1. Distribución Gaussiana, estimando esperanza y varianza")
            print ("2. Intervalos variables, basados en orden y distribución")

        op = int( input() )
        return op
def printMissing(modelType):

    op = 0

    print ("")
    print ("-> Elija una opción para tratar valores continuos: ")

    if modelType == ModelType.DECISION_TREE:
        print ("1. Reemplazar por valor más probable")
        print ("2. Asignar probabilidades a cada rama")

    elif modelType == ModelType.NAIVE_BAYES:
        print ("1. Agregar un m-estimador para normalizar probabilidades")
        print ("2. Ignorar valores faltantes")

    elif modelType == ModelType.KNN:
        print ("1. Reemplazar por valor más probable")
        print ("2. Ignorar valores faltantes")

    op = int( input() )
    return op
def printNorm(modelType):

    if modelType != ModelType.KNN:
        return 3
    else:
        print ("")
        print ("-> Elija una opción para normalizar: ")

        print ("1. Norma euclídea")
        print ("2. Min-max")
        print ("3. Z-score")

        op = int( input() )
        return op

# Main
# --------------------------------------------------------------------------------
if __name__ == '__main__':

    op = 1
    classifiers = []

    while op > 0 and op < 4:

        printMenu(classifiers)
        op = int( input("-> Elija una opción: ") )

        if op < 1 or op > 3:
            sys.exit()

        elif op == 1:

            modelType, modelName = printModelType()
            k = printK(modelType)
            continuous = printContinuous(modelType)
            missing = printMissing(modelType)
            m = printM(modelType, missing)
            norm = printNorm(modelType)

            ds = get_dataset(0)
            model = Model(modelType)

            print()
            print("-> COMIENZO DEL ENTRENAMIENTO")

            tic = time.time()
            model.train(ds, continuous, missing, norm, k, m)
            toc = time.time()

            print("-> FIN DEL ENTRENAMIENTO")
            print("--> Modelo de entrenamiento: ", end="")
            print(modelName)
            print("--> Tiempo de entrenamiento: ", end="")
            print(toc-tic)

            classifier = {
                'model': model,
                'type': modelType,
                'name': modelName,
                'time': toc-tic,
                'continuous' : continuous,
                'missing' : missing,
                'norm' : norm,
                'k' : k,
                'm' : m
            }
            classifiers.append(classifier)

            print()
            input("-> Oprima enter para volver al menú")

        elif op == 2:

            classifiers_aux = []
            for classifier in classifiers:
                if classifier['model'].model != ModelType.KNN:
                    classifiers_aux.append(classifier)

            if classifiers_aux == []:
                print()
                print ("-> No hay clasificadores, entrene uno para clasificar")
                print ("-> NOTA: Clasificadores KNN no cuentan")
                input("-> Oprima enter para volver al menú")
            else:
                printClear()
                printClassifiers(classifiers_aux)

                c = int( input("-> Elija un clasificador por el índice: ") )
                print("")

                if c >= 0 and c < len(classifiers_aux):

                    print("-> Lista de atributos del clasificador: ")
                    print(classifiers_aux[c]['model'].attributes)
                    print()

                    text = input("-> Ingrese un ejemplo, con los atributos separados por ',':\n")
                    example = get_example(text, classifiers_aux[c]['model'].attributes)

                    print()
                    print("-> COMIENZO DE LA CLASIFICACIÓN")

                    model = classifiers_aux[c]['model']

                    tic = time.time()
                    res = model.classify(example, classifiers_aux[c]['continuous'], classifiers_aux[c]['missing'], classifiers_aux[c]['norm'], classifiers_aux[c]['k'], classifiers_aux[c]['m'])
                    toc = time.time()

                    print("-> FIN DE LA CLASIFICACIÓN")
                    print("--> Modelo de clasificador: ", end="")
                    print(classifiers_aux[c]['name'])
                    print("--> Tiempo de clasificación: ", end="")
                    print(toc-tic)
                    print("--> Resultado de clasificación: ", end="")
                    print(res)

                else:
                    print("-> El índice ingresado no corresponde a ningún clasificador")

                print()
                input("-> Oprima enter para volver al menú")
                
        elif op == 3:
  
            if classifiers == []:
                print()
                print ("-> No hay clasificadores, entrene uno para evaluar")
                input("-> Oprima enter para volver al menú")
            else:
                printClear()
                printClassifiers(classifiers)

                c = int( input("-> Elija un clasificador por índice: ") )
                print("")

                print ("-> Elija un algoritmo de validación: ")
                print ("1. Validación normal")
                print ("2. Validación cruzada")
                e = int( input() )

                ds = get_dataset(0)

                if e == 1:
                    (results, confusion_matrix) = normal_validation(ds, classifiers[c])

                    print()
                    print("-> Matriz de confusión:")
                    print("      +    -")
                    print("  +   " + str(confusion_matrix['correct_pos'])+"   "+str(confusion_matrix['incorrect_neg']))
                    print("  -   " + str(confusion_matrix['incorrect_pos'])+"   "+str(confusion_matrix['correct_neg']))

                    print()
                    print("-> Accuracy: " + str(results['accuracy']) )

                    print()
                    print ("-> Positivos: Total {} \n--> Precisión: {} \n--> Recall: {} \n--> MedidaF: {}"
                            .format(results['total_true'], results['precision_true'], results['recall_true'], results['f_true']))

                    print()
                    print ("->Negativos: Total {} \n--> Precisión: {} \n--> Recall: {} \n--> MedidaF: {}"
                           .format(results['total_false'], results['precision_false'], results['recall_false'], results['f_false']))

                elif e == 2:
                    print()
                    k = int(input("-> Elija cantidad de particiones para validación cruzada: "))
                    (results_array, results_mean) = cross_validation(ds, classifiers[c], k)
                    
                    for idx, (results, confusion_matrix) in enumerate(results_array):
                        print()
                        print("########## Validación cruzada, iteración ", idx, " ##########################")

                        print()
                        print("-> Matriz de confusión:")
                        print("      +    -")
                        print("  +   " + str(confusion_matrix['correct_pos'])+"   "+str(confusion_matrix['incorrect_neg']))
                        print("  -   " + str(confusion_matrix['incorrect_pos'])+"   "+str(confusion_matrix['correct_neg']))

                        print()
                        print("-> Accuracy: " + str(results['accuracy']) )

                        print()
                        print ("-> Positivos: Total {} \n--> Precisión: {} \n--> Recall: {} \n--> MedidaF: {}"
                                .format(results['total_true'], results['precision_true'], results['recall_true'], results['f_true']))

                        print()
                        print ("->Negativos: Total {} \n--> Precisión: {} \n--> Recall: {} \n--> MedidaF: {}"
                               .format(results['total_false'], results['precision_false'], results['recall_false'], results['f_false']))

                    print()
                    print("########## Validación cruzada, promedio ##########################")

                    print()
                    print("-> Accuracy: " + str(results_mean['accuracy']) )

                    print()
                    print ("-> Positivos: Total {} \n--> Precisión: {} \n--> Recall: {} \n--> MedidaF: {}"
                            .format(results_mean['total_true'], results_mean['precision_true'], results_mean['recall_true'], results_mean['f_true']))

                    print()
                    print ("->Negativos: Total {} \n--> Precisión: {} \n--> Recall: {} \n--> MedidaF: {}"
                           .format(results_mean['total_false'], results_mean['precision_false'], results_mean['recall_false'], results_mean['f_false']))

                print()
                input("-> Enter to go to main menu")
