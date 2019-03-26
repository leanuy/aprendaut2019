### DEPENDENCIAS
### ------------------

import math

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
    true_results = [(k, (value, probability)) for k, (value, probability) in clasification.items() if value == True]
    print(true_results)
    if len(true_results) == 1:
        (key, (value, probability)) = true_results[0]
        return (key, probability)
    # else: # Hay que votar

    return True
    
### METODOS AUXILIARES
### -------------------

