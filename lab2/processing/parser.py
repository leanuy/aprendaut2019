### DEPENDENCIAS
### ------------------

import copy
import operator
import pandas as pd
from scipy.io import arff

from .calculator import getDiscretePossibleValues

from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES
### -------------------

# A
def getFormattedDataset(dataset, attributes, continuous):
    
    formattedDataset = copy.deepcopy(dataset)
    
    for attribute in attributes:

        (attributeKey, attributeType) = attribute
        values = getDiscretePossibleValues(formattedDataset, attribute, continuous)

        for example in formattedDataset:
            if attributeType == AttributeType.CONTINUOUS:
                for value in values:
                    if value == 'bigger' or example[attributeKey] <= value:
                        example[attributeKey] = value
                        break

    return formattedDataset

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