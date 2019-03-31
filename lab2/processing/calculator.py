### DEPENDENCIAS
### ------------------

import math
import copy
import operator

from utils.const import AttributeType, ContinuousOps, MeasureType


### METODOS AUXILIARES - MEJOR ATRIBUTO
### -----------------------------------

# A
def getBestAttribute(datasetLength, attributes, examplesForValue, proportionsForValue, proportionsForResult, continuous, measure):
  
    (bestAttribute, bestAttributeType) = attributes[0]
    bestExamples = examplesForValue[bestAttribute]
    bestProportions = proportionsForValue[bestAttribute]
    bestValues = list(bestExamples.keys())
    bestValues.remove('bigger')
    bestValues.sort()
    bestValues.append('bigger')

    for attribute in attributes[1:]:
        (attributeKey, attributeType) = attribute
        examples = examplesForValue[attributeKey]
        proportions = proportionsForValue[attributeKey]
        values = list(examples.keys())
        values.remove('bigger')
        values.sort()
        values.append('bigger')
        if getMeasure(datasetLength, examples, proportions, proportionsForResult, measure) > getMeasure(datasetLength, bestExamples, bestProportions, proportionsForResult, measure):
            bestAttribute = attributeKey
            bestAttributeType = attributeType
            bestValues = values

    return ((bestAttribute, bestAttributeType), bestValues)

# A
def getMeasure(datasetLength, examplesForValue, proportionsForValue, proportionsForResult, measure):

    if measure == MeasureType.GAIN:
        return getGain(datasetLength, examplesForValue, proportionsForValue, proportionsForResult)
    elif measure == MeasureType.GAINRATIO:
        return getGainRatio(datasetLength, examplesForValue, proportionsForValue, proportionsForResult)
    elif measure == MeasureType.IMPURITYREDUCTION:
        return getImpurityReduction(datasetLength, examplesForValue, proportionsForValue, proportionsForResult)

### METODOS AUXILIARES - GANANCIA
### -----------------------------

# A
def getGain(datasetLength, examplesForValue, proportionsForValue, proportionsForResult):
    entropy = 0
    for value in examplesForValue:
        entropy += ((len(examplesForValue[value]) / datasetLength) * getEntropy(proportionsForValue[value]))
    return (getEntropy(proportionsForResult) - entropy)

# A
def getEntropy(proportionsForResult):
    entropy = 0
    for p in proportionsForResult:
        if proportionsForResult[p] != 0:
            entropy += -proportionsForResult[p] * math.log(proportionsForResult[p],2)
    return entropy


### METODOS AUXILIARES - RATIO DE GANANCIA
### ----------------------------------------

# A
def getGainRatio(datasetLength, examplesForValue, proportionsForValue, proportionsForResult):
    gainRatio = getGain(datasetLength, examplesForValue, proportionsForValue, proportionsForResult)
    return gainRatio / getSplitInformation(datasetLength, examplesForValue)

def getSplitInformation(datasetLength, examplesForValue):

    proportions = []
    for value in examplesForValue:
        proportions.append(len(examplesForValue[value]) / datasetLength)

    splitInfo = 0
    for p in proportions:
        if p != 0:
            splitInfo += -p * math.log(p,2)

    if splitInfo == 0:
        return 1
    else:
        return splitInfo

### METODOS AUXILIARES - REDUCCIÓN DE IMPUREZA
### ------------------------------------------

# A
def getImpurityReduction(datasetLength, examplesForValue, proportionsForValue, proportionsForResult):
    entropy = 0
    for value in examplesForValue:
        entropy += ((len(examplesForValue[value]) / datasetLength) * getGini(proportionsForValue[value]))
    return (getGini(proportionsForResult) - entropy)

# A
def getGini(proportionsForValue):
    props2 = 0
    for result in proportionsForValue:
        props2 += proportionsForValue[result] ** 2
    return 1 - props2