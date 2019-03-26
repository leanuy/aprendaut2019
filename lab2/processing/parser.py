### DEPENDENCIAS
### ------------------

import copy
import operator
import pandas as pd
from scipy.io import arff

from .reader import getDiscretePossibleValues

from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES
### -------------------

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

