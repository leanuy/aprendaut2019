### DEPENDENCIAS
### ------------------

import time
import math
import random
import numpy as np

from processing.processor import getAllProportionExamplesForResults
from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES
### -------------------

def normalValidation(dataset, classifier):

    shuffled = randomDataset(dataset)
    (trainingSet, evaluationSet) = splitDataset(shuffled, 0.8)
    evaluationSet.drop(columns=['class'])

    print()
    print("-> COMIENZO DEL ENTRENAMIENTO")
    tic = time.time()
    classifier['model'].train(trainingSet, classifier['attributes'], classifier['results'], classifier['options'])
    toc = time.time()
    print("-> FIN DEL ENTRENAMIENTO")
    print()

    print()
    print("-> COMIENZO DE LA CLASIFICACIÓN")
    resultSet = classifier['model'].classifySet(evaluationSet)
    print("-> FIN DE LA CLASIFICACIÓN")
    print()

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

    accuracyMean = 0
    meansMean = (0, 0, 0, 0)
    wMeansMean = (0, 0, 0, 0)
    metricsMean = {}
    for result in results:
        metricsMean[result] = (0, 0, 0, 0)
    
    shuffled = randomDataset(dataset)
    partitions = splitDatasetK(shuffled, k)

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
        (trainingTime, accuracy, means, wMeans, metrics, confusionMatrix) = evaluation

        # Promedio de accuracy
        accuracyMean += accuracy

        # Promedio de promedios generales
        (generalPrecision, generalRecall, generalFalloff, generalFmeasure) = means
        (generalPrecisionMean, generalRecallMean, generalFalloffMean, generalFmeasureMean) = meansMean

        generalPrecisionMean += generalPrecision
        generalRecallMean += generalRecall
        generalFalloffMean += generalFalloff
        generalFmeasureMean += generalFmeasure
        meansMean = (generalPrecisionMean, generalRecallMean, generalFalloffMean, generalFmeasureMean)

        # Promedio de promedios ponderados
        (weightedPrecision, weightedRecall, weightedFalloff, weightedFmeasure) = wMeans
        (weightedPrecisionMean, weightedRecallMean, weightedFalloffMean, weightedFmeasureMean) = wMeansMean
        weightedPrecisionMean += weightedPrecision
        weightedRecallMean += weightedRecall
        weightedFalloffMean +=weightedFalloff
        weightedFmeasureMean += weightedFmeasure
        wMeansMean = (weightedPrecisionMean, weightedRecallMean, weightedFalloffMean, weightedFmeasureMean)

        # Promedio de métricas para cada clase
        for result in metrics:
            (precision, recall, falloff, Fmeasure) = metrics[result]
            (precisionMean, recallMean, falloffMean, FmeasureMean) = metricsMean[result]
            precisionMean += precision
            recallMean += recall
            falloffMean += falloff
            FmeasureMean += Fmeasure
            metricsMean[result] = (precisionMean, recallMean, falloffMean, FmeasureMean)

    # Promedio de accuracy
    accuracyMean /= k

    # Promedio de promedios generales
    (generalPrecisionMean, generalRecallMean, generalFalloffMean, generalFmeasureMean) = meansMean
    generalPrecisionMean /= k
    generalRecallMean /= k
    generalFalloffMean /= k
    generalFmeasureMean /= k
    meansMean = (generalPrecisionMean, generalRecallMean, generalFalloffMean, generalFmeasureMean)

    # Promedio de promedios ponderados
    (weightedPrecisionMean, weightedRecallMean, weightedFalloffMean, weightedFmeasureMean) = wMeansMean
    weightedPrecisionMean /= k
    weightedRecallMean /= k
    weightedFalloffMean /= k
    weightedFmeasureMean /= k
    wMeansMean = (weightedPrecisionMean, weightedRecallMean, weightedFalloffMean, weightedFmeasureMean)

    # Promedio de métricas para cada clase
    for result in metricsMean:
        (precisionMean, recallMean, falloffMean, FmeasureMean) = metricsMean[result]
        precisionMean = precisionMean / k
        recallMean = recallMean / k
        falloffMean = falloffMean / k
        FmeasureMean = FmeasureMean / k
        metricsMean[result] = (precisionMean, recallMean, falloffMean, FmeasureMean)
    
    evaluationsMean = (accuracyMean, meansMean, wMeansMean, metricsMean)
            
    return (evaluations, evaluationsMean)

### METODOS AUXILIARES - CONJUNTOS
### --------------------------------

def randomDataset(dataset):
    return dataset.sample(frac=1)

def splitDataset(dataset, percentage):
    length = len(dataset.index)
    cutPoint = math.floor(percentage * length)
    return (dataset.iloc[:cutPoint], dataset.iloc[cutPoint:])

def splitDatasetK(dataset, k):
    partitions = []
    length = len(dataset.index)

    for i in range(0, k):
        cutFrom = math.floor(i * (1 / k) * length)
        cutTo = math.floor((i+1) * (1 / k) * length)
        
        evaluationSet = dataset.iloc[cutFrom:cutTo]
        trainingSet = dataset.iloc[:cutFrom].append(dataset.iloc[cutTo:])

        partitions.append((trainingSet, evaluationSet))
    
    return partitions

### METODOS AUXILIARES - EVALUACIONES
### ---------------------------------

def getEvaluation(resultSet, evaluationSet, results, trainingTime):

    # Generar matriz de confusión de largo len(results)
    confusionMatrix = getConfusionMatrix(resultSet, evaluationSet, results)

    # Generar diccionario con resultados de evaluación, almacenando 5¿4 resultados:
    # 1. Precision
    # 2. Recall
    # 3. Fall-off
    # 4. Medida F
    evaluation = {}

    # Inicializar promedio de cada medida
    precisionMean = 0
    recallMean = 0
    falloffMean = 0
    FmeasureMean = 0

    # Inicializar promedio ponderado de cada medida
    precisionWeightedMean = 0
    recallWeightedMean = 0
    falloffWeightedMean = 0
    FmeasureWeightedMean = 0

    # Obtener proporciones de ejemplos en el conjunto de evaluación
    proportions = getAllProportionExamplesForResults(evaluationSet, results)

    # Generar dichas medidas para cada posible clase 'result'
    for result in results:

        # Obtener primero los valores TP, FP, TN, FN
        trueResult = getTrueResultClassification(confusionMatrix, results, result)
        falseResult = getFalseResultClassification(confusionMatrix, results, result)
        trueNotResult = getTrueNotResultClassification(confusionMatrix, results, result)
        falseNotResult = getFalseNotResultClassification(confusionMatrix, results, result)

        # Generar medidas y cargarlas en el diccionario para 'result'
        precision = getPrecision(trueResult, falseResult)
        recall = getRecall(trueResult, falseNotResult)
        falloff = getFalloff(falseResult, trueNotResult)
        Fmeasure = getFMeasure(precision, recall)
        evaluation[result] = (precision, recall, falloff, Fmeasure)

        # Sumar a los promedios
        precisionMean += precision
        recallMean += recall
        falloffMean += falloff
        FmeasureMean += Fmeasure

        # Sumar a los promedios ponderados
        precisionWeightedMean += precision * proportions[result]
        recallWeightedMean += recall * proportions[result]
        falloffWeightedMean += falloff * proportions[result]
        FmeasureWeightedMean += Fmeasure * proportions[result]

    # Obtener promedio de cada medida
    resultsLength = len(results)
    precisionMean /= resultsLength
    recallMean /= resultsLength
    falloffMean /= resultsLength
    FmeasureMean /= resultsLength
    means = (precisionMean, recallMean, falloffMean, FmeasureMean)
    
    # Obtener promedio ponderado de cada medida
    weightedMeans = (precisionWeightedMean, recallWeightedMean, falloffWeightedMean, FmeasureWeightedMean)
    
    # Obtener accuracy total
    correctTotal = getAllTrueResultClassification(confusionMatrix)
    accuracy = getAccuracy(correctTotal, len(resultSet))

    return (trainingTime, accuracy, means, weightedMeans, evaluation, confusionMatrix)

### METODOS AUXILIARES - MATRIZ DE CONFUSION
### ----------------------------------------

def getConfusionMatrix(resultSet, evaluationSet, results):
    classes = len(results)
    confusionMatrix = np.zeros((classes, classes), dtype=object)

    evaluationSet['class2'] = resultSet['class']
    
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

def getTrueNotResultClassification(confusionMatrix, results, result):
    withoutRow = np.delete(confusionMatrix, (results.index(result)), axis=0)
    withoutColumn = np.delete(confusionMatrix, (results.index(result)), axis=1)
    return withoutColumn.sum()

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

def getFalloff(fp, tn):
    if fp + tn == 0: return 0
    return fp/(fp + tn)

def getFMeasure(precision, recall):
    if precision + recall == 0: return 0
    return (2*precision*recall)/(precision+recall)

def getAccuracy(tr, total):
    return tr / total
