### DEPENDENCIAS
### ------------------

import math
import copy
import operator
import pandas as pd
from scipy.io import arff

from utils.const import AttributeType, IRIS_DATASET, COVERTYPE_DATASET

### METODOS PRINCIPALES
### -------------------

# Lee 'filename' y lo devuelve como un dataframe de pandas optimizado
# Si el dataset es CoverType, deshace el one hot encoding de sus atributos
def readDataset(filename, isCovertype = False, onehot = False):

    if not isCovertype:
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

        return (optimizedData, attributes, results)

    else:
        data, meta = arff.loadarff(filename)
        data = pd.DataFrame(data)

        optimizedData = pd.DataFrame()

        # Optimización de float
        dataFloat = data.select_dtypes(include=['float'])
        convertedFloat = dataFloat.apply(pd.to_numeric,downcast='float')
        optimizedData[convertedFloat.columns] = convertedFloat

        # Optimización de int
        dataObject = data.select_dtypes(include=['object']).copy()
        dataObject = dataObject.drop(columns=['class'])
        convertedObject = pd.DataFrame()
        for col in dataObject.columns:
            convertedObject.loc[:,col] = dataObject[col].astype('int')
        convertedObject = dataObject.apply(pd.to_numeric,downcast='unsigned')

        if onehot:
            # Optimización de one hot encoding
            attribute1 = convertedObject.iloc[:, :4]
            attribute2 = convertedObject.iloc[:, 4:]

            attribute1 = attribute1[attribute1==1].stack().reset_index().drop(0,1)
            attribute1 = attribute1['level_1']
            attribute1 = attribute1.apply(getColumnValue).astype('uint8')
            attribute1 = attribute1.astype('uint8')
            optimizedData['wilderness_area'] = attribute1

            attribute2 = attribute2[attribute2==1].stack().reset_index().drop(0,1)
            attribute2 = attribute2['level_1']
            attribute2 = attribute2.apply(getColumnValue)
            attribute2 = attribute2.astype('uint8')
            optimizedData['soil_type'] = attribute2
        
        else:
            optimizedData[convertedObject.columns] = convertedObject

        # Optimización de category
        dataClassification = data['class']
        convertedClassification = dataClassification.astype('category')
        optimizedData['class'] = convertedClassification

        attributes = getAttributesDecoded(optimizedData.columns)
        results = getResults(data)

        return (optimizedData, attributes, results)

### METODOS AUXILIARES - ATRIBUTOS
### ---------------------------------

# Devuelve la lista de posibles atributos y su tipo en 'dataset'
def getAttributes(meta):
    return list(zip(meta.names()[:-1], [ AttributeType.CONTINUOUS if x == 'numeric' else AttributeType.DISCRETE for x in meta.types()[:-1] ] ))

# Devuelve la lista de posibles atributos y su tipo en 'dataset'
# para CoverType sin one hot encoding
def getAttributesDecoded(columns):
    attributes = list(columns)[:-1]
    return list(zip(attributes, [ AttributeType.CONTINUOUS for x in columns ] ))

### METODOS AUXILIARES - RESULTADOS
### ---------------------------------

# Devuelve la lista de posibles clasificaciones en 'dataset'
def getResults(data):
    return sorted(list(set(data['class'])))

### METODOS AUXILIARES - OPTIMIZACIÓN
### ---------------------------------

# Función a aplicar en pandas dataframe, obtiene el número
# de atributo para 'wilderness_area' y 'soil_type'
def getColumnValue(column):
    values = column.split('_')
    return int(values[2])