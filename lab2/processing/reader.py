### DEPENDENCIAS
### ------------------

import math
import copy
import operator
import pandas as pd
from scipy.io import arff

import .calculator as calculator
from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES
### -------------------

# Lee 'dsFile' y lo devuelve como un diccionario (atributo, valor)
def readDataset(filename):
    ds = arff.loadarff(filename)
    df = pd.DataFrame(ds[0])
    ds = df.to_dict('records')
    return ds

### METODOS PRINCIPALES - ATRIBUTOS
### ---------------------------------

# Devuelve la lista de posibles atributos y su tipo en 'dataset'
def getAttributes(dataset):
    attributes = set()
    example = dataset[0]
    for key in list(example.keys()):
        if key != 'class':
            attribute = str(key)
            attributeType = checkAttributeType(getAllPossibleValues(dataset, attribute))
            attributes.add((attribute, attributeType))
    return list(attributes)

# Devuelve la lista de posibles valores en 'dataset' para 'attribute'
def getPossibleValues(dataset, attribute):
    (attributeKey, attributeType) = attribute
    values = []
    for x in dataset:
        if x[attributeKey] not in values:
          values.append(x[attributeKey])
    return values

# Devuelve la lista de posibles valores (discretizados) en 'dataset' para 'attribute'
def getDiscretePossibleValues(dataset, attribute, continuous):

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

        # Iterate through sorted training examples, adding a new value to whenever the answer changes
        # adding the median value between the current value and the previous one
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

        # Iterate through sorted training examples, adding a new value to whenever the answer changes
        # adding the median value between the current value and the previous one
        for example in sortedDataset:
            if lastRes != None and example['class'] != lastRes:
                possibleValues.append(((float(example[attributeKey]) - float(lastExample)) / 2) + float(lastExample))
            lastRes = example['class']
            lastExample = example[attributeKey]

        bestGain = 0
        bestThreshold = None
        results = getResults(dataset)
        for value in possibleValues:
            valueThreshold = [value, 'bigger']
            gain = calculator.getGain(dataset, attribute, valueThreshold, results)
            if gain > bestGain:
                bestGain = gain
                bestThreshold = value
        return [bestThreshold, 'bigger']

# Devuelve la lista de posibles valores discretos en 'dataset' para 'attribute'
def getAllPossibleValues(dataset, attribute):
    possibleValues = set()
    for x in dataset:
        possibleValues.add(x[attribute])
    return list(possibleValues)

# Devuelve la lista de posibles valores para todos los atributos dde 'dataset'
def getDatasetPossibleValues(dataset, attributes):
    values = {}
    for attribute in attributes:
        (attributeKey, attributeType) = attribute
        attributeValues = getPossibleValues(dataset, attribute)
        # Si es un atributo continuo, ordena la lista de atributos
        if attributeType == AttributeType.CONTINUOUS:
            attributeValues = sorted([str(x) for x in attributeValues])
            attributeValues = [float(x) for x in attributeValues if x != 'bigger']
            attributeValues.append('bigger')
        values[attributeKey] = attributeValues
    return values

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
def proportionExamplesForValue(dataset, attribute, values, value):
    if len(dataset) == 0:
      return 0
    examples = getExamplesForValue(dataset, attribute, values, value)
    return len(examples) / len(dataset)

### METODOS PRINCIPALES - RESULTADOS
### ---------------------------------

# Devuelve la lista de posibles clasificaciones en 'dataset'
def getResults(dataset):
    results = set()
    for x in dataset:
        results.add(x['class'])
    return sorted(list(results))
  
# Devuelve el resultado de 'results' más frecuente en 'dataset'
def getMostLikelyResult(dataset, results):

    mostLikelyResult = results[0]
    mostLikelyProportion = proportionExamplesForResult(dataset, results[0])

    for result in results[1:]:
        proportion = proportionExamplesForResult(dataset, result)
        if proportion >= mostLikelyProportion:
            mostLikelyResult = result
            mostLikelyProportion = proportion

    return (mostLikelyResult, mostLikelyProportion)

# Devuelve la frecuencia de ejemplos en 'dataset' clasificados como 'result'
def proportionExamplesForResult(dataset, result):
    if len(dataset) == 0:
      return 0
    examples = [x for x in dataset if x['class'] == result]
    return len(examples) / len(dataset)

### METODOS PRINCIPALES - CONTINUIDAD
### ---------------------------------

# Devuelve el tipo de atributo basado en sus posibles valores
def checkAttributeType(possibleValues):

    example = possibleValues[0]
    if type(example) != int and type(example) != float:
        return AttributeType.DISCRETE
    else:
        booleanSet = {0, 1}
        valuesSet = set(possibleValues)
        if booleanSet == valuesSet:
          return AttributeType.DISCRETE
        else:
          return AttributeType.CONTINUOUS
