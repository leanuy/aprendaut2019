### DEPENDENCIAS
### ------------------

import math
import random
from operator import itemgetter

from .node import Node
from .decision_tree import id3Train, id3Classify

import processing.reader as reader
import processing.parser as parser

from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES
### -------------------

def id3ForestTrain(dataset, attributes, values, results, continuous): 

    forest = {}
    for result in results:
        resultDataset = parser.getBooleanDataset(dataset, result)
        resultResults = [True, False]
        forest[result] = id3Train(resultDataset, attributes, values, resultResults, continuous)

    return forest

def id3ForestClassify(forest, example, results, continuous):

    clasification = {}
    for result in results:
        clasification[result] = id3Classify(forest[result], example, continuous)

    true_results = [(key, (value, probability)) for key, (value, probability) in clasification.items() if value == True]
    if len(true_results) == 1:
        (key, (value, probability)) = true_results[0]
        return (key, probability)
    elif len(true_results) > 1:
        (best_key, (best_value, best_probability)) =  max(true_results,key=itemgetter(1))
        best_results = [(key, (value, probability)) for key, (value, probability) in clasification.items() if probability == best_probability]
        if len(best_results) == 1:
            (key, (value, probability)) = best_results[0]
        elif len(best_results) > 1:
            (key, (value, probability)) = random.choice(best_results)
        return (key, probability)

    # Nunca deberia llegar aca
    return False
    
### METODOS AUXILIARES
### -------------------

