### DEPENDENCIAS
### ------------------

import math
import copy
import operator
import pandas as pd
from scipy.io import arff

from . import calculator
from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES
### -------------------

# Lee 'dsFile' y lo devuelve como un diccionario (atributo, valor)
def readDataset(filename):
    ds = arff.loadarff(filename)
    #print(ds)
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
            attributeType = calculator.checkAttributeType(calculator.getAllPossibleValues(dataset, attribute))
            attributes.add((attribute, attributeType))
    return list(attributes)


### METODOS PRINCIPALES - RESULTADOS
### ---------------------------------

# Devuelve la lista de posibles clasificaciones en 'dataset'
def getResults(dataset):
    results = set()
    for x in dataset:
        results.add(x['class'])
    return sorted(list(results))
  