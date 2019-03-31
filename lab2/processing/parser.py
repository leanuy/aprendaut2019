### DEPENDENCIAS
### ------------------

import copy
import operator
import pandas as pd
from scipy.io import arff

from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES - DATASET
### -----------------------------

# A 
def getBooleanDataset(dataset, result):
    
    formattedDataset = dataset.copy()
    formattedDataset['class'] = formattedDataset['class'].apply(changeResult, args=(result,))

    return formattedDataset

### METODOS PRINCIPALES - EJEMPLOS
### ------------------------------

# A
def getFormattedExample(text, attributes):
    values = text.split(",")
    example = {}
    i = 0
    for attribute in attributes:
        example[attribute] = float(values[i])
        i = i + 1
    return example

### METODOS AUXILIARES
### ------------------------------

def changeResult(value, result):
    return value == result
    

