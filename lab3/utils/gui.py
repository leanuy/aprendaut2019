### DEPENDENCIAS
### ------------------

import os
import sys

from .const import MenuOps, ModelOps, ContinuousOps, MeasureOps, DistanceOps, NormOps, EvaluationOps, IRIS_DATASET, COVERTYPE_DATASET

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
    print ("#######################################################")
    print ("#                                                     #")
    print ("#        MENÚ - Laboratorio 3 (Clasificadores)        #")
    print ("#                                                     #")
    print ("#######################################################")
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
        modelType = c['type']
        
        print("")
        print("-> ", end="")
        print(str(index), end="")
        print(" - ", end="")
        print("Clasificador ", end="")
        print(c['name'])

        if modelType == ModelOps.KNN:
            print("   Cantidad de vecinos: ", end="")
            print(c['options']['k'])

        if modelType != ModelOps.KNN:
            print("   Estrategia de atributos continuos: ", end="")
            print(c['options']['continuous'])

        if modelType != ModelOps.NAIVE_BAYES:
            print("   Estrategia de medida: ", end="")
            print(c['options']['measure'])

        if modelType == ModelOps.KNN:
            print("   Estrategia de normalización: ", end="")
            print(c['options']['norm'])

        if modelType == ModelOps.NAIVE_BAYES or modelType == ModelOps.KNN:
            print("   Estrategia de one hot encoding: ", end="")
            print(c['options']['onehot'])

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
    print ("1. Árbol de decisión")
    print ("2. Bosque de decisión")
    print ("3. Bayes sencillo")
    print ("4. K vecinos más cercanos")

    try:
        modelType = int( input() )

        if modelType < 1 or modelType > 4:
            return (ModelOps.DECISION_TREE, "Árbol")
        else:
            if modelType == 1:
                modelType = ModelOps.DECISION_TREE
                modelName = "Árbol"
            elif modelType == 2:
                modelType = ModelOps.DECISION_FOREST
                modelName = "Bosque"
            elif modelType == 3:
                modelType = ModelOps.NAIVE_BAYES
                modelName = "Bayes"
            elif modelType == 4:
                modelType = ModelOps.KNN
                modelName = "KNN"

        return (modelType, modelName)

    except:
        return (ModelOps.DECISION_TREE, "Árbol")

# Imprime las opciones de vecinos y lee la opción elegida
def printModelK(modelType):
    if modelType != ModelOps.KNN:
        return 3
    else:
        print ("")
        print ("-> Elija cantidad de vecinos para evaluar: ")
        print ("-> DEFAULT: 3")
        try:
            evaluationK = int( input() )
            return evaluationK
        except:
            return 3

# Imprime las estrategias para tratar atributos continuos y lee la opción elegida
def printContinuousStrategy(modelType):
    
    if modelType == ModelOps.KNN:
        return ContinuousOps.FIXED

    elif modelType == ModelOps.NAIVE_BAYES:
        print ("")
        print ("-> Elija una estrategia para tratar atributos continuos: ")
        print ("-> DEFAULT: 1")
        print ("1. Estandarizar según distribución N(0,1)")
        print ("2. Partir en intervalos variables (según clasificación)")

        try:
            continuousStrategy = int( input() )

            if continuousStrategy < 1 or continuousStrategy > 2:
                return ContinuousOps.STANDARDIZATION
            else:
                if continuousStrategy == 1:
                    continuousStrategy = ContinuousOps.STANDARDIZATION
                elif continuousStrategy == 2:
                    continuousStrategy = ContinuousOps.VARIABLE

            return continuousStrategy

        except:
            return ContinuousOps.STANDARDIZATION

    else:
        print ("")
        print ("-> Elija una estrategia para tratar atributos continuos: ")
        print ("-> DEFAULT: 1")
        print ("1. Partir en intervalos fijos (según mediana, en 2)")
        print ("2. Partir en intervalos variables (según clasificación)")
        print ("3. Partir en intervalos maximizando ganancia (según C4.5)")

        try:
            continuousStrategy = int( input() )

            if continuousStrategy < 1 or continuousStrategy > 3:
                return ContinuousOps.FIXED
            else:
                if continuousStrategy == 1:
                    continuousStrategy = ContinuousOps.FIXED
                elif continuousStrategy == 2:
                    continuousStrategy = ContinuousOps.VARIABLE
                elif continuousStrategy == 3:
                    continuousStrategy = ContinuousOps.C45

            return continuousStrategy

        except:
            return ContinuousOps.FIXED

# Imprime las opciones de medidas posibles y lee la opción elegida
def printMeasureType(modelType):

    if modelType == ModelOps.NAIVE_BAYES:
        return MeasureOps.GAIN

    elif modelType == ModelOps.KNN:
        print ("")
        print ("-> Elija un tipo de medida de distancia: ")
        print ("-> DEFAULT: 2")
        print ("1. Distancia 'Manhattan'")
        print ("2. Distancia Euclídea")
        print ("3. Distancia de Chebychev")
        print ("4. Distancia de Mahalanobis")

        try:
            measureType = int( input() )
            if measureType == 1:
                return DistanceOps.MANHATTAN
            elif measureType == 2:
                return DistanceOps.EUCLIDEAN
            elif measureType == 3:
                return DistanceOps.CHEBYCHEV
            elif measureType == 4:
                return DistanceOps.MAHALANOBIS
            return DistanceOps.EUCLIDEAN

        except:
            return DistanceOps.EUCLIDEAN

    else:
        print ("")
        print ("-> Elija un tipo de medida: ")
        print ("-> DEFAULT: 1")
        print ("1. Gain")
        print ("2. Gain Ratio")
        print ("3. Impurity Reduction")

        try:
            measureType = int( input() )
            if measureType == 1:
                return MeasureOps.GAIN
            elif measureType == 2:
                return MeasureOps.GAINRATIO
            elif measureType == 3:
                return MeasureOps.IMPURITYREDUCTION
            return MeasureOps.GAIN

        except:
            return MeasureOps.GAIN

# Imprime las opciones de normalización posibles y lee la opción elegida
def printNormType(modelType):

    if modelType != ModelOps.KNN:
        return NormOps.EUCLIDEAN

    else:
        print ("")
        print ("-> Elija un tipo de normalización: ")
        print ("-> DEFAULT: 1")
        print ("1. Norma Euclídea (División por norma)")
        print ("2. Norma Min-Max (Reescalamiento)")
        print ("3. Norma Z-Score (Estandarización)")
        print ("0. Ninguna")

        try:
            measureType = int( input() )
            if measureType == 1:
                return NormOps.EUCLIDEAN
            elif measureType == 2:
                return NormOps.MIN_MAX
            elif measureType == 3:
                return NormOps.Z_SCORE
            elif measureType == 0:
                return NormOps.NONE
            return NormOps.EUCLIDEAN

        except:
            return NormOps.EUCLIDEAN

# Imprime las opciones de vecinos y lee la opción elegida
def printOneHotEncoding(modelType):
    if modelType == ModelOps.DECISION_TREE or modelType == ModelOps.DECISION_FOREST:
        return True
    else:
        print ("")
        print ("-> Desea revertir el One Hot Encoding (si existe)? (y/n): ")
        print ("-> DEFAULT: y")
        try:
            onehot = input()
            return onehot != 'n'
        except:
            return True

# Imprime los datos de entrenamiento de un clasificador
def printTrainedClassifier(classifier):

    modelType = classifier['type']

    print("-> Modelo Entrenado - ", end="")
    print(classifier['name'])

    print("--> Tiempo de entrenamiento: ", end="")
    print(classifier['time'], end=" ")
    print("segundos")

    if modelType == ModelOps.KNN:
        print("--> Cantidad de vecinos: ", end="")
        print(classifier['options']['k'])

    if modelType != ModelOps.KNN:
        print("--> Estrategia de atributos continuos: ", end="")
        print(classifier['options']['continuous'])

    if modelType != ModelOps.NAIVE_BAYES:
        print("--> Estrategia de medida: ", end="")
        print(classifier['options']['measure'])

    if modelType == ModelOps.KNN:
        print("--> Estrategia de normalización: ", end="")
        print(classifier['options']['norm'])

    if modelType == ModelOps.NAIVE_BAYES or modelType == ModelOps.KNN:
        print("--> Estrategia de one hot encoding: ", end="")
        print(classifier['options']['onehot'])

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

# Imprime las opciones de particiones de evaluación y lee la opción elegida
def printEvaluationK():
    print ("")
    print ("-> Elija cantidad de particiones para evaluar: ")
    print ("-> DEFAULT: 10")
    try:
        evaluationK = int( input() )
        return evaluationK
    except:
        return 10

# Imprime datos de evaluación
def printEvaluation(classifier, accuracy, means, weightedMeans, eval, confusionMatrix):
    
    print("-> Accuracy: ", end="")
    print(accuracy)
    print()

    print("-> Promedio general de métricas: ")
    (precisionMean, recallMean, falloffMean, FmeasureMean) = means
    print("--> Precision promediada: ", end="")
    print(precisionMean)
    print("--> Recall promediada: ", end="")
    print(recallMean)        
    print("--> Fall-off promediada: ", end="")
    print(falloffMean)
    print("--> F-Measure promediada: ", end="")
    print(FmeasureMean)
    print()

    print("-> Promedio ponderado de métricas: ")
    (precisionWMean, recallWMean, falloffWMean, FmeasureWMean) = weightedMeans
    print("--> Precision ponderada: ", end="")
    print(precisionWMean)
    print("--> Recall ponderada: ", end="")
    print(recallWMean)        
    print("--> Fall-off ponderada: ", end="")
    print(falloffWMean)
    print("--> F-Measure ponderada: ", end="")
    print(FmeasureWMean)
    print()

    print("-> Confusion Matrix: ")
    print()
    printConfusionMatrix(confusionMatrix, classifier['results'])

    for result in eval:
        print()
        print("-> Evaluación para ", end="")
        print(result, end=": ")
        print()

        (precision, recall, falloff, Fmeasure) = eval[result]
        print("--> Precision: ", end="")
        print(precision)
        print("--> Recall: ", end="")
        print(recall)        
        print("--> Fall-off: ", end="")
        print(falloff)
        print("--> F-Measure: ", end="")
        print(Fmeasure)
        
    print()

# Imprime una matriz de confusión dada para un vector de posibles clases
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

# Imprime datos genéricos de evaluación normal y llama a printEvaluation
def printNormalEvaluation(classifier, trainingTime, accuracy, means, weightedMeans, eval, confusionMatrix, dataLength):
    print()
    print("MODELO:")
    print()
    print("-> Modelo Entrenado: ", end="")
    print(classifier['name'])
    print("-> Estrategia de atributos continuos: ", end="")
    print(classifier['options']['continuous'])
    print("-> Estrategia de medida: ", end="")
    print(classifier['options']['measure'])
    print("-> Tiempo de entrenamiento: ", end="")
    print(trainingTime)
    print()
    print("EVALUACIÓN NORMAL (80/20):")
    print()
    trainingLength = (dataLength // 5) * 4
    evaluationLength = dataLength // 5
    print("-> Total de ejemplos: " + str(dataLength))
    print("-> Ejemplos de entrenamiento: " + str(trainingLength))
    print("-> Ejemplos de evaluación: " + str(evaluationLength))
    print()
    printEvaluation(classifier, accuracy, means, weightedMeans, eval, confusionMatrix)

# Imprime datos genéricos de evaluación cruzada y llama a printEvaluation para cada iteración
def printCrossEvaluation(classifier, eval, evalMean, dataLength):
    print()
    print("MODELO:")
    print()
    print("-> Modelo Entrenado: ", end="")
    print(classifier['name'])
    print("-> Estrategia de atributos continuos: ", end="")
    print(classifier['options']['continuous'])
    print("-> Estrategia de medida: ", end="")
    print(classifier['options']['measure'])
    print()
    print("EVALUACIÓN CRUZADA (" + str(len(eval)) + " particiones):")
    print()
    trainingLength = (dataLength // len(eval)) * (len(eval) - 1)
    evaluationLength = dataLength // len(eval)
    print("-> Total de ejemplos: " + str(dataLength))
    print("-> Ejemplos de entrenamiento: " + str(trainingLength))
    print("-> Ejemplos de evaluación: " + str(evaluationLength))
    print()
    for i in range(0, len(eval)):
        print()
        print("--- Partición N° " + str(i+1) + " ---")
        print()
        (trainingTime, accuracyK, meansK, wMeansK, evalK, confusionMatrixK) = eval[i]
        printEvaluation(classifier, accuracyK, meansK, wMeansK, evalK, confusionMatrixK)
    
    print()
    print("--- Promedio de Evaluación ---")
    print()
    
    (accuracy, meansMean, wMeansMean, metricsMean) = evalMean
    print("-> Accuracy: ", end="")
    print(accuracy)
    print()

    print("-> Promedio de métricas promediadas: ")
    (precisionMean, recallMean, falloffMean, FmeasureMean) = meansMean
    print("--> Precision general promediada: ", end="")
    print(precisionMean)
    print("--> Recall general promediada: ", end="")
    print(recallMean)        
    print("--> Fall-off general promediada: ", end="")
    print(falloffMean)
    print("--> F-Measure general promediada: ", end="")
    print(FmeasureMean)
    print()

    print("-> Promedio de métricas ponderadas: ")
    (precisionWMean, recallWMean, falloffWMean, FmeasureWMean) = wMeansMean
    print("--> Precision general ponderada: ", end="")
    print(precisionWMean)
    print("--> Recall general ponderada: ", end="")
    print(recallWMean)        
    print("--> Fall-off general ponderada: ", end="")
    print(falloffWMean)
    print("--> F-Measure general ponderada: ", end="")
    print(FmeasureWMean)
    print()

    for result in metricsMean:
        print()
        print("-> Evaluación para ", end="")
        print(result, end=": ")
        print()
        (precision, recall, falloff, Fmeasure) = metricsMean[result]
        print("--> Precision: ", end="")
        print(precision)
        print("--> Recall: ", end="")
        print(recall)   
        print("--> Fall-off: ", end="")
        print(falloff)        
        print("--> F-Measure: ", end="")
        print(Fmeasure)
    print()