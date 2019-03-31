### DEPENDENCIAS
### ------------------

import math

from .node import Node

import processing.processor as processor
import processing.calculator as calculator

from utils.const import AttributeType, ContinuousOps, MeasureOps, CONTINUOUS, MEASURE

### METODOS PRINCIPALES
### -------------------

def id3Train(dataset, attributes, results, options):

    # Caso Borde: Todos los ejemplos son de una clase
    (result, proportion) = processor.getMostLikelyResult(dataset, results)
    if proportion == 1:
        return (result, proportion)

    # Caso Borde: No hay más atributos a evaluar
    elif len(attributes) == 0:
        return (result, proportion)

    # No hay caso borde
    else:

        # 1. Obtener atributo con mayor ganancia de información y sus posibles valores
        (attribute, values) = getBestAttribute(dataset, attributes, results, options)
        (attributeKey, attributeType) = attribute

        # 2. Generar lista de atributos nueva y diccionario de hijos
        newAttributes = list(attributes)
        newAttributes.remove(attribute)
        branches = {}

        # 3. Iterar por cada posible valor para el atributo elegido
        for value in values:

            # 3.1. Obtener el subconjunto de ejemplos para el valor 'value' del atributo 'attribute'
            examplesForValue = processor.getExamplesForValue(dataset, attribute, values, value)

            # 3.2. Si no hay ejemplos, devolver hoja con el resultado más frecuente (y su probabilidad)
            if len(examplesForValue) == 0:
                branches[value] = processor.getMostLikelyResult(dataset, results)

            # 3.3. Si hay ejemplos, devolver rama generada recursivamente
            else:
                branches[value] = id3Train(examplesForValue, newAttributes, results, options)

        # 4. Devolver nodo intermedio
        return Node(attribute, branches)

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
def getBestAttribute(dataset, attributes, results, options):

    continuous = options[CONTINUOUS]

    bestAttributeKey = None
    bestAttributeType = None
    bestValues = None

    for attribute in attributes:
        (attributeKey, attributeType) = attribute
        possibleValues = processor.getDiscretePossibleValues(dataset, attribute, results, continuous, calculator.getGain)
        
        if bestAttributeKey != None:
            thisMeasure = getMeasure(dataset, attribute, possibleValues, results, options)
            bestMeasure = getMeasure(dataset, (bestAttributeKey, bestAttributeType), bestValues, results, options)

        if bestAttributeKey == None or thisMeasure > bestMeasure:
            bestAttributeKey = attributeKey
            bestAttributeType = attributeType
            bestValues = possibleValues
    
    return ((bestAttributeKey, bestAttributeType), bestValues)

# A
def getMeasure(dataset, attribute, possibleValues, results, options):
    measure = options[MEASURE]
    if measure == MeasureOps.GAIN:
        return calculator.getGain(dataset, attribute, possibleValues, results)
    elif measure == MeasureOps.GAINRATIO:
        return calculator.getGainRatio(dataset, attribute, possibleValues, results)
    elif measure == MeasureOps.IMPURITYREDUCTION:
        return calculator.getImpurityReduction(dataset, attribute, possibleValues, results)
