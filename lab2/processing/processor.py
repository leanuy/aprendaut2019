### DEPENDENCIAS
### ------------------

import math
import copy
import operator

from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES - ATRIBUTOS
### ---------------------------------

# Devuelve la lista de posibles valores en 'dataset' para 'attribute'
def getPossibleValues(dataset, attribute):
    (attributeKey, attributeType) = attribute
    values = []
    for x in dataset:
        if x[attributeKey] not in values:
          values.append(x[attributeKey])
    return values

# Devuelve la lista de posibles valores (discretizados) en 'dataset' para 'attribute'
def getDiscretePossibleValues(dataset, attribute, results, continuous, getGain):

    (attributeKey, attributeType) = attribute
    sortedDataset = sorted(dataset, key=operator.itemgetter(attributeKey))
    values = getPossibleValues(sortedDataset, attribute)

    if attributeType == AttributeType.DISCRETE:
        return values
    
    elif attributeType == AttributeType.CONTINUOUS and continuous == ContinuousOps.FIXED:

        median = len(values) // 2

        possibleValues = []
        possibleValues.append(values[median])
        possibleValues.append("bigger")

        return possibleValues

    elif attributeType == AttributeType.CONTINUOUS and continuous == ContinuousOps.VARIABLE:

        possibleValues = []
        lastRes = None
        lastExample = None

        for example in sortedDataset:
            if lastRes != None and example['class'] != lastRes:
                possibleValues.append(((float(example[attributeKey]) - float(lastExample)) / 2) + float(lastExample))
            lastRes = example['class']
            lastExample = example[attributeKey]
        possibleValues.append("bigger")

        return possibleValues
    elif attributeType == AttributeType.CONTINUOUS and continuous == ContinuousOps.C45:
        possibleValues = []
        lastRes = None
        lastExample = None

        for example in sortedDataset:
            if lastRes != None and example['class'] != lastRes:
                possibleValues.append(((float(example[attributeKey]) - float(lastExample)) / 2) + float(lastExample))
            lastRes = example['class']
            lastExample = example[attributeKey]

        bestGain = 0
        bestThreshold = None
        for value in possibleValues:
            valueThreshold = [value, 'bigger']
            gain = getGain(dataset, attribute, valueThreshold, results)
            if gain > bestGain:
                bestGain = gain
                bestThreshold = value
        return [bestThreshold, 'bigger']

### METODOS PRINCIPALES - EJEMPLOS
### ---------------------------------

# Devuelve el subconjunto de 'dataset' con valor 'value' en el atributo 'attribute'
def getExamplesForValue(dataset, attribute, values, value):
    (attributeKey, attributeType) = attribute

    if attributeType == AttributeType.CONTINUOUS and value == 'bigger':
        index = values.index(value)
        return [x for x in dataset if x[attributeKey] > values[index-1]]

    elif attributeType == AttributeType.CONTINUOUS and value != 'bigger':
        return [x for x in dataset if x[attributeKey] <= value]

    else:
        return [x for x in dataset if x[attributeKey] == value]

# Devuelve la frecuencia de ejemplos en 'dataset' con 'attribute'='value'
def getProportionExamplesForValue(dataset, attribute, values, value):
    if len(dataset) == 0:
      return 0
    examples = getExamplesForValue(dataset, attribute, values, value)
    return len(examples) / len(dataset)

### METODOS PRINCIPALES - RESULTADOS
### ---------------------------------
  
# Devuelve el resultado de 'results' más frecuente en 'dataset'
def getMostLikelyResult(dataset, results):

    proportions = getAllProportionExamplesForResults(dataset, results)
    
    mostLikelyResult = None
    mostLikelyProportion = 0

    for key, value in proportions.items():
        if value >= mostLikelyProportion:
            mostLikelyResult = key
            mostLikelyProportion = value

    return (mostLikelyResult, mostLikelyProportion)

# Devuelve la frecuencia de ejemplos en 'dataset' clasificados como 'result'
def getProportionExamplesForResult(dataset, result):
    if len(dataset) == 0:
      return 0
    examples = [x for x in dataset if x['class'] == result]
    return len(examples) / len(dataset)

# Devuelve las frecuencias de ejemplos en 'dataset' para todos los resultados en 'results'
def getAllProportionExamplesForResults(dataset, results):
    resultsHash = {}
    for result in results:
        resultsHash[result] = []
    for x in dataset:
        result = x['class']
        resultsHash[result].append(x)
    proportions = {}
    for result in results:
        proportions[result] = len(resultsHash[result]) / len(dataset)
    return proportions