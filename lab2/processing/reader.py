### DEPENDENCIAS
### ------------------

import math
import copy
import operator
import pandas as pd
from scipy.io import arff

from utils.const import AttributeType

### METODOS PRINCIPALES
### -------------------

# Lee 'dsFile' y lo devuelve como un diccionario (atributo, valor)
def readDataset(filename):
    data, meta = arff.loadarff(filename)
    data = pd.DataFrame(data)

    attributes = getAttributes(meta)
    results = getResults(data)

    # Optimización de float
    dataFloat = data.select_dtypes(include=['float'])
    convertedFloat = dataFloat.apply(pd.to_numeric,downcast='float')

    # Optimización de int
    dataObject = data.select_dtypes(include=['object']).copy()
    dataObject = dataObject.drop(columns=['class'])
    convertedObject = pd.DataFrame()
    for col in dataObject.columns:
        convertedObject.loc[:,col] = dataObject[col].astype('int')
    convertedObject = dataObject.apply(pd.to_numeric,downcast='unsigned')

    # Optimización de category
    dataClassification = data['class']
    convertedClassification = dataClassification.astype('category')

    optimizedData = data.copy()
    optimizedData[convertedFloat.columns] = convertedFloat
    optimizedData[convertedObject.columns] = convertedObject
    optimizedData['class'] = convertedClassification    

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
