### DEPENDENCIAS
### ------------------

import math
import random
import numpy as np

import processing.reader as reader
from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES
### -------------------

def normalValidation(dataset, classifier):

    (trainingSet, evaluationSet) = splitDataset(dataset, 20, 0.8)
    
    evalSet = []
    for example in evaluationSet:
        d = dict(example)
        d.pop('class', None)
        evalSet.append(d)

<<<<<<< HEAD
    classifier['model'].train(trainingSet, classifier['attributes'], classifier['results'], classifier['options'])
=======
    classifier['model'].train(trainingSet, classifier['continuous'], classifier['measureType'])
>>>>>>> 1cefabf70fdb4bb664d4c47f07cf200e4ecf77b5
    resultSet = classifier['model'].classifySet(evalSet)

    return getEvaluation(resultSet, evaluationSet, classifier['results'])

def crossValidation(dataset, classifier, k):

    validator = list(dataset)
    random.seed(20)
    random.shuffle(validator)

    partitions = [validator[i::k] for i in range(0,k)]
    results = classifier['results']
    evaluations = []

    metricsMean = {}
    for result in results:
        metricsMean[result] = (0, 0, 0)
    evaluationsMean = (0, metricsMean)

    # Generar 'k' evaluaciones
    for i in range(0,k):

        # Generar conjunto de entrenamiento y evaluación para la iteración 'i'
        trainingSet = []
        evaluationSet = partitions[i]
        for idx, partition in enumerate(partitions):
            if idx != i:
                trainingSet.extend(partition)

        evalSet = []
        for example in evaluationSet:
            d = dict(example)
            d.pop('class', None)
            evalSet.append(d)

<<<<<<< HEAD
        classifier['model'].train(trainingSet, classifier['attributes'], classifier['results'], classifier['options'])
=======
        classifier['model'].train(trainingSet, classifier['continuous'], classifier['measureType'])
>>>>>>> 1cefabf70fdb4bb664d4c47f07cf200e4ecf77b5
        resultSet = classifier['model'].classifySet(evalSet)

        # Evaluar el modelo entrenado
        evaluations.append(getEvaluation(resultSet, evaluationSet, results))

    # Generar promedio de las 'k' evaluaciones
    for evaluation in evaluations:
        (accuracy, metrics, confusionMatrix) = evaluation
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

def splitDataset(dataset, randSeed, percentage):

    shuffled = list(dataset)

    random.seed(randSeed)
    random.shuffle(shuffled)

    length = len(shuffled)
    cutPoint = math.floor(percentage * length)
    return (shuffled[:cutPoint], shuffled[cutPoint:])

### METODOS AUXILIARES - EVALUACIONES
### ---------------------------------

def getEvaluation(resultSet, evaluationSet, results):

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

    return (accuracy, evaluation, confusionMatrix)

### METODOS AUXILIARES - MATRIZ DE CONFUSION
### ----------------------------------------

def getConfusionMatrix(resultSet, evaluationSet, results):
    classes = len(results)
    confusionMatrix = np.zeros((classes, classes), dtype=object)

    for i in range(len(resultSet)):

        classifiedExample = resultSet[i]
        originalExample = evaluationSet[i]

        if classifiedExample['class'] != None and originalExample['class'] != None:
            (classification, probability) = classifiedExample['class']
            originalClassification = originalExample['class']

            i = results.index(classification)
            j = results.index(originalClassification)
            confusionMatrix[i][j] += 1

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
