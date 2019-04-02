### DEPENDENCIAS
### ------------------

import copy
import operator
import pandas as pd
from scipy.io import arff

from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES - DATASET
### -----------------------------

# Formatea 'dataset' sustituyendo la clasificación 
# para 'result' por True y todas las demás por False
def getBooleanDataset(dataset, result):
    
    formattedDataset = dataset.copy()
    formattedDataset['class'] = formattedDataset['class'].apply(changeResult, args=(result,))

    return formattedDataset

### METODOS PRINCIPALES - EJEMPLOS
### ------------------------------

# Formatea un 'text' basandose en 'attributes' para
# devolver un ejemplo interpretable por un clasificador
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

# Función a aplicar en pandas dataframe, obtiene el número
# de atributo para 'wilderness_area' y 'soil_type'
def changeResult(value, result):
    return value == result
    

