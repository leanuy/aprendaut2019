### DEPENDENCIAS
### ------------------

import random
import math

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

def cross_validation(ds, model, k):

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

### METODOS AUXILIARES
### -------------------

def splitDataset(dataset, randSeed, percentage):

    shuffled = list(dataset)

    random.seed(randSeed)
    random.shuffle(shuffled)

    length = len(shuffled)
    cutPoint = math.floor(percentage * length)
    return (shuffled[:cutPoint], shuffled[cutPoint:])

def getEvaluation(resultSet, evaluationSet, results):

    # Generar diccionario con resultados de evaluación, almacenando 7 resultados:
    # 1. Clasificados correctamente como 'result'
    # 2. Clasificados incorrectamente como 'result'
    # 3. Clasificados como 'result' (total)
    # 4. Clasificados incorrectamente como distinto a 'result'
    # 5. Precision
    # 6. Recall
    # 7. Medida F
    evaluation = {}
    for result in results:
        evaluation[result] = ((0, 0, 0), 0, (0, 0, 0))

    # Comparar cada ejemplo clasificado con su verdadera clasificación
    for i in range(len(resultSet)):

        classifiedExample = resultSet[i]
        originalExample = evaluationSet[i]
        
        (classification, probability) = classifiedExample['class']
        originalClassification = originalExample['class']

        ((correct, incorrect, total), aux, others) = evaluation[classification]
        total += 1
        if classification == originalClassification:
            correct += 1
        else:
            incorrect += 1

        evaluation[classification] = ((correct, incorrect, total), aux, others)

    # Obtener clasificados incorrectamente para cada resultado
    for result in results:
        for i in range(len(evaluationSet)):
            classifiedExample = resultSet[i]
            originalExample = evaluationSet[i]

            (classification, probability) = classifiedExample['class']
            originalClassification = originalExample['class']
            
            if originalClassification == result and classification != result:
                (others1, falseNegative, others2) = evaluation[result]
                falseNegative += 1
                evaluation[result] = (others1, falseNegative, others2)
 
    # Obtener precision, recall y medida F para cada resultado
    for result in results:
        ((correct, incorrect, total), falseNegative, (precision, recall, Fmeasure)) = evaluation[result]
        precision = getPrecision(correct, incorrect)
        recall = getRecall(correct, falseNegative)
        Fmeasure = getFMeasure(precision, recall)
        evaluation[result] = ((correct, incorrect, total), falseNegative, (precision, recall, Fmeasure))

    # Obtener accuracy total
    correctTotal = 0
    incorrectTotal = 0
    for result in results:
        ((correct, incorrect, total), aux, others) = evaluation[result]
        correctTotal = correct
        incorrectTotal = incorrect
  
    accuracy = getAccuracy(correctTotal, incorrectTotal, len(resultSet))

    return (evaluation, accuracy)

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
