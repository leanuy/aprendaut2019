# Dependencias
# --------------------------------------------------------------------------------

import random
import math
from model import Model, ModelType
from preprocessor import *

# Métodos principales
# --------------------------------------------------------------------------------

def normal_validation(ds, model):

    dataset = ds
    if model['model'].model == ModelType.KNN:
        dataset = one_hot_encode_ds(ds)
        if model['missing'] == 1:
            fill_missing_values(dataset, get_attributes_from_dataset(dataset))

    (train, evaluate) = split_data(dataset, 20, 0.8)

    print("Training with: " + str(len(train) + " elements")
    print("Evaluating with: " + str(len(evaluate) + " elements")
    
    classify_array = []
    for example in evaluate:
        d = dict(example)
        d.pop('truth', None)
        classify_array.append(d)

    print()
    print("-> COMIENZO DE ENTRENAMIENTO")

    tic = time.time()
    model['model'].train(train, model['continuous'], model['missing'], model['norm'], model['k'], model['m'], True)
    toc = time.time()

    print("-> FIN DE ENTRENAMIENTO")
    print(tic-toc)
    print()

    print()
    print("-> COMIENZO DE CLASIFICACIÓN")

    tic = time.time()
    result = model['model'].classify_set(classify_array, model['continuous'], model['missing'], model['norm'], model['k'], model['m'])
    toc = time.time()

    print("-> FIN DE CLASIFICACIÓN")
    print(tic-toc)
    print()

    return get_results(result, evaluate)

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

# Métodos auxiliares
# --------------------------------------------------------------------------------

def split_data(ds, randSeed, percentage):
    random.seed(randSeed)

    # Mezclar ejemplos
    shuffled = list(ds)
    random.shuffle(shuffled)

    length = len(shuffled)
    cut_point = math.floor(percentage * length)
    return (shuffled[:cut_point], shuffled[cut_point:])

def get_results(examples, evaluation_dataset):
    cant_examples = len(examples)

    cant_negativos_predecidos_incorrectos = 0
    cant_negativos_predecidos_correctos = 0
    total_negativos = 0

    cant_positivos_predecidos_incorrectos = 0
    cant_positivos_predecidos_correctos = 0
    total_positivos = 0

    for i in range(len(examples)):

        if evaluation_dataset[i]['truth'] == True:
            total_positivos += 1
            if examples[i] == True:
                cant_positivos_predecidos_correctos += 1
            else:
                cant_positivos_predecidos_incorrectos += 1

        if evaluation_dataset[i]['truth'] == False:
            total_negativos += 1
            if examples[i] == False:
                cant_negativos_predecidos_correctos += 1
            else:
                cant_negativos_predecidos_incorrectos += 1

    # Precisión, recall y medida f para True
    precision_true = precision (cant_positivos_predecidos_correctos, cant_positivos_predecidos_incorrectos)
    recall_true    = recall(cant_positivos_predecidos_correctos, cant_negativos_predecidos_incorrectos)
    f_true         = f_score(precision_true, recall_true)

    # Precisión, recall y medida f para False
    precision_false = precision (cant_negativos_predecidos_correctos, cant_negativos_predecidos_incorrectos)
    recall_false    = recall(cant_negativos_predecidos_correctos, cant_positivos_predecidos_incorrectos)
    f_false          = f_score(precision_false, recall_false)

    acc = accuracy(cant_positivos_predecidos_correctos, cant_negativos_predecidos_correctos,
                        cant_positivos_predecidos_incorrectos, cant_negativos_predecidos_incorrectos)

    confusion_matrix = {
        'correct_pos': cant_positivos_predecidos_correctos,
        'incorrect_pos': cant_positivos_predecidos_incorrectos,
        'correct_neg': cant_negativos_predecidos_correctos,
        'incorrect_neg': cant_negativos_predecidos_incorrectos
    }

    results = {
        'total_true': cant_positivos_predecidos_correctos+cant_negativos_predecidos_incorrectos,
        'total_false': cant_negativos_predecidos_correctos+cant_positivos_predecidos_incorrectos,
        'precision_true': precision_true,
        'precision_false': precision_false,
        'recall_true': recall_true,
        'recall_false': recall_false,
        'f_true': f_true,
        'f_false': f_false,
        'accuracy': acc
    }

    return (results, confusion_matrix)

def precision(true_positives,false_positives):
    if true_positives + false_positives == 0: return -1
    return true_positives/(true_positives + false_positives)

def recall(true_positives, false_negatives):
    if true_positives + false_negatives == 0: return -1
    return true_positives/(true_positives + false_negatives)

def f_score(precision, recall):
    return (2*precision*recall)/(precision+recall)

def accuracy(true_positives, true_negatives, false_positives, false_negatives):
    return (true_positives + true_negatives) / (true_positives + true_negatives + false_positives + false_negatives)
