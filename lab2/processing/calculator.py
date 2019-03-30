### DEPENDENCIAS
### ------------------

import math

import .reader as reader
from utils.const import MeasureType

### METODOS PRINCIPALES - MEJOR ATRIBUTO
### -----------------------------------

# A
def getBestAttribute(dataset, attributes, results, continuous, measureType):
  
    (bestAttribute, bestAttributeType) = attributes[0]
    bestValues = reader.getDiscretePossibleValues(dataset, attributes[0], continuous)

    for attribute in attributes[1:]:
        (attributeKey, attributeType) = attribute
        possibleValues = reader.getDiscretePossibleValues(dataset, attribute, continuous)
        if getMeasure(dataset, attribute, possibleValues, results, measureType) > getMeasure(dataset, (bestAttribute, bestAttributeType), bestValues, results, measureType):
            bestAttribute = attributeKey
            bestAttributeType = attributeType
            bestValues = possibleValues

    return ((bestAttribute, bestAttributeType), bestValues)

# A
def getMeasure(dataset, attribute, possibleValues, results, measureType):

    if measureType == MeasureType.GAIN:
        return getGain(dataset, attribute, possibleValues, results)
    elif measureType == MeasureType.GAINRATIO:
        return getGainRatio(dataset, attribute, possibleValues, results)
    elif measureType == MeasureType.IMPURITYREDUCTION:
        return getImpurityReduction(dataset, attribute, possibleValues, results)

### METODOS PRINCIPALES - GANANCIA
### -----------------------------

# A
def getGain(dataset, attribute, possibleValues, results):
    
    entropy = 0
    for value in possibleValues:
        subset = reader.getExamplesForValue(dataset, attribute, possibleValues, value)
        entropy += ((len(subset)/len(dataset)) * getEntropy(subset, results))

    return (getEntropy(dataset, results) - entropy)

# A
def getEntropy(dataset, results):

    proportions = []
    for result in results:
        proportions.append(reader.proportionExamplesForResult(dataset, result))

    entropy = 0
    for p in proportions:
        if p != 0:
            entropy += -p * math.log(p,2)

    return entropy


### METODOS PRINCIPALES - RATIO DE GANANCIA
### ----------------------------------------

# A
def getGainRatio(dataset, attribute, possibleValues, results):

    gainRatio = getGain(dataset, attribute, possibleValues, results)
    if getEntropy(dataset, results) != 0:
        gainRatio /= getSplitInformation(dataset, attribute, possibleValues)

    return gainRatio

def getSplitInformation(dataset, attribute, possibleValues):

    proportions = []
    for value in possibleValues:
        proportions.append(reader.proportionExamplesForValue(dataset, attribute, possibleValues, value))

    splitInfo = 0
    for p in proportions:
        if p != 0:
            splitInfo += -p * math.log(p,2)

    return splitInfo

### METODOS PRINCIPALES - REDUCCIÓN DE IMPUREZA
### ------------------------------------------

# A
def getImpurityReduction(dataset, attribute, possibleValues, results):
    
    entropy = 0
    for value in possibleValues:
        subset = reader.getExamplesForValue(dataset, attribute, possibleValues, value)
        entropy += ((len(subset)/len(dataset)) * getGini(subset, results))

    return (getGini(dataset, results) - entropy)

# A
def getGini(dataset, results):

    props2 = 0
    for result in results:
        props2 += reader.proportionExamplesForResult(dataset, result) ** 2

    return 1 - props2