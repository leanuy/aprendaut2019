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

    i = 0
    for index, example in formattedDataset.iterrows():
        classification = example['class']
        formattedDataset.iloc[i, formattedDataset.columns.get_loc('class')] = classification == result
        i += 1

    return formattedDataset

def getDecodedDataset(dataset, attributes, results):
    
    formattedDataset = copy.deepcopy(dataset)
    
    for example in formattedDataset:
        classification = example['class']
        example['class'] = classification == result

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

