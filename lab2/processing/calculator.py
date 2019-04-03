### DEPENDENCIAS
### -----------------------------------

import math

from . import processor
from utils.const import MeasureOps

### METODOS AUXILIARES - GANANCIA
### -----------------------------

# Obtener ganancia de 'attribute' en 'dataset'
def getGain(dataset, attribute, possibleValues, results):
    entropy = 0
    for value in possibleValues:
        subset = processor.getExamplesForValue(dataset, attribute, possibleValues, value)
        entropy += ((len(subset.index)/len(dataset.index)) * getEntropy(subset, results))

    return (getEntropy(dataset, results) - entropy)

# Obtener entropía de 'dataset'
def getEntropy(dataset, results):

    proportions = []
    for result in results:
        proportions.append(processor.getProportionExamplesForResult(dataset, result))

    entropy = 0
    for p in proportions:
        if p != 0:
            entropy += -p * math.log(p,2)

    return entropy

### METODOS AUXILIARES - RATIO DE GANANCIA
### ----------------------------------------

# Obtener ratio de ganancia de 'attribute' en 'dataset'
def getGainRatio(dataset, attribute, possibleValues, results):

    gainRatio = getGain(dataset, attribute, possibleValues, results)
    if getEntropy(dataset, results) != 0:
        gainRatio /= getSplitInformation(dataset, attribute, possibleValues)

    return gainRatio

# Obtener métrica auxiliar para ratio de ganancia en 'dataset'
def getSplitInformation(dataset, attribute, possibleValues):

    proportions = []
    for value in possibleValues:
        proportions.append(processor.getProportionExamplesForValue(dataset, attribute, possibleValues, value))

    splitInfo = 0
    for p in proportions:
        if p != 0:
            splitInfo += -p * math.log(p,2)

    if splitInfo == 0:
        splitInfo = 1

    return splitInfo

### METODOS AUXILIARES - REDUCCIÓN DE IMPUREZA
### ------------------------------------------

# Obtener reducción de impureza de 'attribute' en 'dataset'
def getImpurityReduction(dataset, attribute, possibleValues, results):
    
    entropy = 0
    for value in possibleValues:
        subset = processor.getExamplesForValue(dataset, attribute, possibleValues, value)
        entropy += ((len(subset.index)/len(dataset.index)) * getGini(subset, results))

    return (getGini(dataset, results) - entropy)

# Obtener métrica auxiliar para reducción de impureza en 'dataset'
def getGini(dataset, results):

    props2 = 0
    for result in results:
        props2 += processor.getProportionExamplesForResult(dataset, result) ** 2

    return 1 - props2