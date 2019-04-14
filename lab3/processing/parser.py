### DEPENDENCIAS
### ------------------

import csv
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

### METODOS PRINCIPALES - ARCHIVOS
### ------------------------------

# Formatea una evaluación generando un CSV para el notebook
def getEvaluationCSV(filename, accuracy, means, wMeans, evals, confusionMatrix = None):
    with open(filename, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL,
                                lineterminator='\n')
        filewriter.writerow([accuracy,"","",""])
        filewriter.writerow(means)
        filewriter.writerow(wMeans)

        for eval in evals:
          filewriter.writerow(evals[eval])

        if confusionMatrix is not None:
            for i in range(0, len(confusionMatrix)):
                filewriter.writerow(confusionMatrix[i])

### METODOS AUXILIARES
### ------------------------------

# Función a aplicar en pandas dataframe, obtiene el número
# de atributo para 'wilderness_area' y 'soil_type'
def changeResult(value, result):
    return value == result
    

