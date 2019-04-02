### DEPENDENCIAS
### ------------------

import time
import math
import random
import numpy as np

import processing.reader as reader
from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES
### -------------------

def normalValidation(dataset, classifier):

    shuffled = randomDataset(dataset)
    (trainingSet, evaluationSet) = splitDataset(shuffled, 0.8)
    
    print()
    print("-> COMIENZO DEL ENTRENAMIENTO")
    tic = time.time()
    classifier['model'].train(trainingSet, classifier['attributes'], classifier['results'], classifier['options'])
    toc = time.time()
    print("-> FIN DEL ENTRENAMIENTO")
    print()

    print("-> COMIENZO DE LA CLASIFICACIÓN")
    resultSet = classifier['model'].classifySet(evaluationSet)
    print("-> FIN DE LA CLASIFICACIÓN")
    print()

    print("-> COMIENZO DE LA EVALUACIÓN")
    evaluation = getEvaluation(resultSet, evaluationSet, classifier['results'], toc-tic)
    print("-> FIN DE LA EVALUACIÓN")
    print()

    return evaluation

def crossValidation(dataset, classifier, k):

    results = classifier['results']
    partitions = []    
    evaluations = []

    metricsMean = {}
    for result in results:
        metricsMean[result] = (0, 0, 0)
    evaluationsMean = (0, metricsMean)
    
    shuffled = randomDataset(dataset)

    # Generar 'k' particiones
    for i in range(0,k):
        (trainingDataset, evaluationDataset) = splitDataset(shuffled, 1 // k)
        partitions.append((trainingDataset, evaluationDataset))

    # Generar 'k' evaluaciones
    for i in range(0,k):

        # Generar conjunto de entrenamiento y evaluación para la iteración 'i'
        (trainingSet, evaluationSet) = partitions[i]

        print()
        print("-> COMIENZO DEL ENTRENAMIENTO N° " + str(i))
        classifier['model'].train(trainingSet, classifier['attributes'], classifier['results'], classifier['options'])
        print("-> FIN DEL ENTRENAMIENTO N° " + str(i))
        print()

        resultSet = classifier['model'].classifySet(evaluationSet)

        # Evaluar el modelo entrenado
        evaluations.append(getEvaluation(resultSet, evaluationSet, results, 0))

    # Generar promedio de las 'k' evaluaciones
    for evaluation in evaluations:
        (accuracy, metrics, confusionMatrix, trainingTime) = evaluation
        (accuracyMean, metricsMean) = evaluationsMean
        accuracyMean += accuracy
        for result in metrics:
            (precision, recall, Fmeasure) = metrics[result]
            (precisionMean, recallMean, FmeasureMean) = metricsMean[result]
            precisionMean += precision
            recallMean += recall
            FmeasureMean += Fmeasure
            metricsMean[result] = (precisionMean, recallMean, FmeasureMean)
        evaluationsMean = (accuracyMean, metricsMean)

    (accuracyMean, metricsMean) = evaluationsMean
    accuracyMean = accuracyMean / k
    for result in metricsMean:
        (precisionMean, recallMean, FmeasureMean) = metricsMean[result]
        precisionMean = precisionMean / k
        recallMean = recallMean / k
        FmeasureMean = FmeasureMean / k
        metricsMean[result] = (precisionMean, recallMean, FmeasureMean)
    evaluationsMean = (accuracyMean, metricsMean)
            
    return (evaluations, evaluationsMean)

### METODOS AUXILIARES - CONJUNTOS
### --------------------------------

def randomDataset(dataset):
    return dataset.sample(frac=1)

def splitDataset(dataset, percentage):
    length = len(dataset.index)
    cutPoint = math.floor(percentage * length)
    print(len(dataset.iloc[:cutPoint]))
    print(len(dataset.iloc[cutPoint:]))
    return (dataset.iloc[:cutPoint], dataset.iloc[cutPoint:])

### METODOS AUXILIARES - EVALUACIONES
### ---------------------------------

def getEvaluation(resultSet, evaluationSet, results, trainingTime):

    # Generar matriz de confusión de largo len(results)
    confusionMatrix = getConfusionMatrix(resultSet, evaluationSet, results)

    # Generar diccionario con resultados de evaluación, almacenando 3 resultados:
    # 1. Precision
    # 2. Recall
    # 3. Medida F
    evaluation = {}

    # Generar dichas medidas para cada posible clase 'result'
    for result in results:

        # Obtener primero
        trueResult = getTrueResultClassification(confusionMatrix, results, result)
        falseResult = getFalseResultClassification(confusionMatrix, results, result)
        falseNotResult = getFalseNotResultClassification(confusionMatrix, results, result)

        # Generasr medidas y cargarlas en el diccionario para 'result'
        precision = getPrecision(trueResult, falseResult)
        recall = getRecall(trueResult, falseNotResult)
        Fmeasure = getFMeasure(precision, recall)
        evaluation[result] = (precision, recall, Fmeasure)

    # Obtener accuracy total
    correctTotal = getAllTrueResultClassification(confusionMatrix)
    accuracy = getAccuracy(correctTotal, len(resultSet))

    return (accuracy, evaluation, confusionMatrix, trainingTime)

### METODOS AUXILIARES - MATRIZ DE CONFUSION
### ----------------------------------------

def getConfusionMatrix(resultSet, evaluationSet, results):
    classes = len(results)
    confusionMatrix = np.zeros((classes, classes), dtype=object)

    evaluationSet['class2'] = resultSet['class']
    print(evaluationSet['class2'])

    print('SADASDASD')
    print(evaluationSet['class'])

    for index in evaluationSet.index:
        class1 = evaluationSet.at[index,'class']
        class2 = evaluationSet.at[index,'class2']
        if class1 != None and class2 != None:
            x = results.index(class1)
            y = results.index(class2)
            confusionMatrix[x][y] += 1
    return confusionMatrix

def getTrueResultClassification(confusionMatrix, results, result):
    i = results.index(result)
    return confusionMatrix[i][i]

def getFalseResultClassification(confusionMatrix, results, result):
    res = 0
    j = results.index(result)
    for i in range(0, len(results)):
        if i != j:
            res += confusionMatrix[i][j]
    return res

def getFalseNotResultClassification(confusionMatrix, results, result):
    res = 0
    i = results.index(result)
    for j in range(0, len(results)):
        if i != j:
            res += confusionMatrix[i][j]
    return res

def getAllTrueResultClassification(confusionMatrix):
    return confusionMatrix.trace()

### METODOS AUXILIARES - MEDIDAS
### ---------------------------------

def getPrecision(tp, fp):
    if tp + fp == 0: return 0
    return tp/(tp + fp)

def getRecall(tp, fn):
    if tp + fn == 0: return 0
    return tp/(tp + fn)

def getFMeasure(precision, recall):
    if precision + recall == 0: return 0
    return (2*precision*recall)/(precision+recall)

def getAccuracy(tr, total):
    return tr / total
