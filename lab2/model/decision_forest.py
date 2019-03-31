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

def id3ForestTrain(dataset, attributes, results, options):

    forest = {}
    for result in results:
        resultDataset = parser.getBooleanDataset(dataset, result)
        resultResults = [True, False]
        forest[result] = id3Train(resultDataset, attributes, resultResults, options)

    return forest

def id3ForestClassify(forest, example, results):

    clasification = {}
    for result in results:
        clasification[result] = id3Classify(forest[result], example)

    trueResults = [(key, (value, probability)) for key, (value, probability) in clasification.items() if value == True]
    if len(trueResults) == 1:
        (key, (value, probability)) = trueResults[0]
        return (key, probability)
    elif len(trueResults) > 1:
        (bestKey, (bestValue, bestProbability)) =  max(trueResults,key=itemgetter(1))
        bestResults = [(key, (value, probability)) for key, (value, probability) in clasification.items() if probability == bestProbability]
        if len(bestResults) == 1:
            (key, (value, probability)) = bestResults[0]
        elif len(bestResults) > 1:
            (key, (value, probability)) = random.choice(bestResults)
        return (key, probability)

    # Nunca deberia llegar aca
    return (random.choice(results), 0.1)