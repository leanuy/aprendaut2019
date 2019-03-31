### DEPENDENCIAS
### ------------------

import copy
import operator
import pandas as pd
from scipy.io import arff

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