### DEPENDENCIAS
### ------------------

import math

from .node import Node

import processing.reader as reader
from utils.const import AttributeType, ContinuousOps, MeasureType

### METODOS PRINCIPALES
### -------------------

def id3Train(dataset, attributes, results, continuous, measureType):

    # Caso Borde: Todos los ejemplos son de una clase
    (result, proportion) = reader.getMostLikelyResult(dataset, results)
    if proportion == 1:
        return (result, proportion)

    # Caso Borde: No hay más atributos a evaluar
    elif len(attributes) == 0:
        return (result, proportion)

    # No hay caso borde
    else:

        # 1. Obtener atributo con mayor ganancia de información y sus posibles valores
        (attribute, values) = getBestAttribute(dataset, attributes, results, continuous, measureType)
        (attributeKey, attributeType) = attribute

        # 2. Generar lista de atributos nueva y diccionario de hijos
        newAttributes = list(attributes)
        newAttributes.remove(attribute)
        options = {}

        # 3. Iterar por cada posible valor para el atributo elegido
        for value in values:

            # 3.1. Obtener el subconjunto de ejemplos para el valor 'value' del atributo 'attribute'
            examplesForValue = reader.getExamplesForValue(dataset, attribute, values, value)

            # 3.2. Si no hay ejemplos, devolver hoja con el resultado más frecuente (y su probabilidad)
            if len(examplesForValue) == 0:
                options[value] = reader.getMostLikelyResult(dataset, results)

            # 3.3. Si hay ejemplos, devolver rama generada recursivamente
            else:
                options[value] = id3Train(examplesForValue, newAttributes, results, continuous, measureType)

        # 4. Devolver nodo intermedio
        return Node(attribute, options)

def id3Classify(tree, example):
    if type(tree) == Node:
        currentAttribute = tree.attribute
        currentAttributeType = tree.attributeType
        currentBranches = list(tree.options.keys())
        for branch in currentBranches:
            if currentAttributeType == AttributeType.DISCRETE:
                if branch == example[currentAttribute]:
                    node = tree.options[branch]
                    if type(node) == Node:
                        return id3Classify(node, example)
                    else:
                        return node
            else:
                value = example[currentAttribute]
                if branch == 'bigger' or value <= branch:
                    node = tree.options[branch]
                    if type(node) == Node:
                        return id3Classify(node, example)
                    else:
                        return node
                    break
    else:
        return tree
    
### METODOS AUXILIARES - MEJOR ATRIBUTO
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

### METODOS AUXILIARES - GANANCIA
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

    proportions = reader.readAllProportionExamplesForResults(dataset)

    entropy = 0
    for p in proportions.values():
        if p != 0:
            entropy += -p * math.log(p,2)

    return entropy


### METODOS AUXILIARES - RATIO DE GANANCIA
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

### METODOS AUXILIARES - REDUCCIÓN DE IMPUREZA
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
    proportions = reader.readAllProportionExamplesForResults(dataset)

    for p in proportions.values():
        props2 += p ** 2

    return 1 - props2