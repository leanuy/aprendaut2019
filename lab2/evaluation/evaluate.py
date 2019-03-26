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

    classifier['model'].train(trainingSet, classifier['continuous'])
    resultSet = classifier['model'].classifySet(evalSet)

    return getEvaluation(resultSet, evaluationSet, classifier['model'].getModelResults())

def crossValidation(dataset, classifier, k):

    validator = list(ds)
    random.seed(20)
    random.shuffle(validator)

    if model['model'].model == ModelType.KNN:
        validator = one_hot_encode_ds(validator)
        if model['missing'] == 1:
            fill_missing_values(validator, get_attributes_from_dataset(validator))

    k_partitions = [validator[i::k] for i in range(0,k)]
    results = []
    result_mean = {}

    for i in range(0,k):
        train_data = []
        test_data = k_partitions[i]
        for idx, partition in enumerate(k_partitions):
            if idx != i:
                train_data.extend(partition)

        # se entrena el modelo
        classify_array = []
        for example in test_data:
            d = dict(example)
            d.pop('truth', None)
            classify_array.append(d)

        model['model'].train(train_data, model['continuous'], model['missing'], model['norm'], model['k'], model['m'], True)
        result = model['model'].classify_set(classify_array, model['continuous'], model['missing'], model['norm'], model['k'], model['m'])

        # evaluo
        r = get_results(result, k_partitions[i])
        results.append(r)

    result_mean['total_true'] = 0
    result_mean['total_false'] = 0
    result_mean['precision_true'] = 0
    result_mean['precision_false'] = 0
    result_mean['recall_true'] = 0
    result_mean['recall_false'] = 0
    result_mean['f_true'] = 0
    result_mean['f_false'] = 0
    result_mean['accuracy'] = 0

    for res in results:
        (r, cm) = res
        result_mean['total_true'] = result_mean['total_true'] + r['total_true']
        result_mean['total_false'] = result_mean['total_false'] + r['total_false']
        result_mean['precision_true'] = result_mean['precision_true'] + r['precision_true']
        result_mean['precision_false'] = result_mean['precision_false'] + r['precision_false']
        result_mean['recall_true'] = result_mean['recall_true'] + r['recall_true']
        result_mean['recall_false'] = result_mean['recall_false'] + r['recall_false']
        result_mean['f_true'] = result_mean['f_true'] + r['f_true']
        result_mean['f_false'] = result_mean['f_false'] + r['f_false']
        result_mean['accuracy'] = result_mean['accuracy'] + r['accuracy']

    for key in result_mean.keys():
        result_mean[key] = result_mean[key] / k

    return (results,result_mean)

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
    incorrectTotal = getAllFalseResultClassification(confusionMatrix)
    accuracy = getAccuracy(correctTotal, incorrectTotal, len(resultSet))

    return (accuracy, evaluation, confusionMatrix)

### METODOS AUXILIARES - MATRIZ DE CONFUSION
### ----------------------------------------

def getConfusionMatrix(resultSet, evaluationSet, results):
    classes = len(results)
    confusionMatrix = np.zeros((classes, classes), dtype=object)

    for i in range(len(resultSet)):

        classifiedExample = resultSet[i]
        originalExample = evaluationSet[i]

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

def getAllFalseResultClassification(confusionMatrix):
    return confusionMatrix.sum() - confusionMatrix.trace()

### METODOS AUXILIARES - MEDIDAS
### ---------------------------------

def getPrecision(tp, fp):
    if tp + fp == 0: return -1
    return tp/(tp + fp)

def getRecall(tp, fn):
    if tp + fn == 0: return -1
    return tp/(tp + fn)

def getFMeasure(precision, recall):
    return (2*precision*recall)/(precision+recall)

def getAccuracy(tp, tn, total):
    return (tp + tn) / total
