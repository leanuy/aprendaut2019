### DEPENDENCIAS
### ------------------

import copy

from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES
### -------------------

# A
def getFormattedExample(text, attributes):
    values = text.split(",")
    example = {}
    i = 0
    for attribute in attributes:
        example[attribute] = float(values[i])
        i = i + 1
    return example

# A 
def getBooleanDataset(dataset, result):
    formattedDataset = copy.deepcopy(dataset)
    for example in formattedDataset:
        classification = example['class']
        example['class'] = classification == result
    return formattedDataset

### METODOS AUXILIARES
### -------------------

# A
def getDiscreteValue(intervals, rawValue):
    value = None
    for interval in intervals[:-1]:
        if rawValue < interval:
            value = interval
            break
    if value == None:
        value = intervals[-1]
    return value


