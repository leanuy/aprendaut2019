### DEPENDENCIAS
### ------------------

import math

from .node import Node
from .decision_tree import id3Train

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

def id3ForestClassify(forest, example, continuous):
    if type(tree) == Node:
        currentAttribute = tree.attribute
        currentAttributeType = tree.attributeType
        currentBranches = list(tree.options.keys())
        for branch in currentBranches:
            if currentAttributeType == AttributeType.DISCRETE:
                if branch == example[currentAttribute]:
                    node = tree.options[branch]
                    if type(node) == Node:
                        return id3Classify(node, example, continuous)
                    else:
                        return node
            else:
                value = example[currentAttribute]
                if branch == 'bigger' or value <= branch:
                    node = tree.options[branch]
                    if type(node) == Node:
                        return id3Classify(node, example, continuous)
                    else:
                        return node
                    break
    else:
        return tree
    
### METODOS AUXILIARES
### -------------------

