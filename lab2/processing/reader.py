### DEPENDENCIAS
### ------------------

import math
import copy
import operator
import pandas as pd
from scipy.io import arff

from . import calculator
from utils.const import AttributeType

### METODOS PRINCIPALES
### -------------------

# Lee 'dsFile' y lo devuelve como un diccionario (atributo, valor)
def readDataset(filename):
    data, meta = arff.loadarff(filename)
    df = pd.DataFrame(data)

    attributes = getAttributes(meta)
    results = getResults(df)

    data = df.to_dict('records')
    return (data, attributes, results)

### METODOS PRINCIPALES - ATRIBUTOS
### ---------------------------------

# Devuelve la lista de posibles atributos y su tipo en 'dataset'
def getAttributes(meta):
    return list(zip(meta.names()[:-1], [ AttributeType.CONTINUOUS if x == 'numeric' else AttributeType.DISCRETE for x in meta.types()[:-1] ] ))

### METODOS PRINCIPALES - RESULTADOS
### ---------------------------------

# Devuelve la lista de posibles clasificaciones en 'dataset'
def getResults(data):
    return sorted(list(set(data['class'])))
  