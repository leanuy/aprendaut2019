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

    classification = {}
    for result in results:
        classification[result] = id3Classify(forest[result], example)

    trueResults = [(key, (value, probability)) for key, (value, probability) in classification.items() if value == True]
    
    if len(trueResults) == 1:
        (key, (value, probability)) = trueResults[0]
        return (key, probability)
    
    elif len(trueResults) > 1:
        (bestKey, (bestValue, bestProbability)) =  max(trueResults,key=itemgetter(1))
        bestResults = [(key, (value, probability)) for key, (value, probability) in classification.items() if probability == bestProbability]
        if len(bestResults) == 1:
            (key, (value, probability)) = bestResults[0]
        elif len(bestResults) > 1:
            (key, (value, probability)) = random.choice(bestResults)
        return (key, probability)

    # En el caso de no poder clasificar, elige una clasificación aleatoria pero con baja probabilidad
    return (random.choice(results), 0.1)