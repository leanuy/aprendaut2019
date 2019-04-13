### DEPENDENCIAS
### ------------------
import math
import time
import random
import numpy as np
from scipy import stats
import processing.processor as processor
import processing.calculator as calculator
from utils.const import AttributeType, ContinuousOps, MeasureOps, CONTINUOUS, MEASURE

### METODOS PRINCIPALES
### -------------------

def nbTrain(dataset, attributes, results, options):
    # Inicialización
    classificator = {}
    amountClass = {}
    mEst = options['mEst']
    proportions = processor.getAllProportionExamplesForResults(dataset, results)

    for result in results:
        classificator[result] = {}
        amountClass[result] = proportions[result] * len(dataset.index)

        # En total se guarda la probabilidad sin considerar atributos
        classificator[result]['total'] = proportions[result]

        for attribute in attributes:
            (attributeKey, attributeType) = attribute
            classificator[result][attributeKey] = {}
            # Atributo continuo y estrategia de estandarización
            if attributeType == AttributeType.CONTINUOUS and options[CONTINUOUS] == ContinuousOps.STANDARDIZATION:
                valuesOfResult = dataset[dataset['class'] == result]
                classificator[result][attributeKey]['mean'] = calculateMean(valuesOfResult, attributeKey)
                classificator[result][attributeKey]['std'] = calculateStandardDeviation(valuesOfResult, attributeKey)
            # Atributo continuo y estrategia de intervalos variables
            elif attributeType == AttributeType.CONTINUOUS and options[CONTINUOUS] == ContinuousOps.VARIABLE:
                for value in processor.getDiscretePossibleValues(dataset, attribute, results, options[CONTINUOUS], None):
                    classificator[result][attributeKey][value] = 0
            # Atributo es discreto
            else:
                for value in processor.getPossibleValues(dataset, attribute):
                    classificator[result][attributeKey][value] = 0               

    # Para cada valor de cada atributo se cuenta la ocurrencia de valores
    for index in dataset.index:
        result = dataset.at[index, 'class']
        for attributeKey, attributeType in attributes:
            # Atributo continuo y estrategia de estandarización
            if attributeType == AttributeType.CONTINUOUS and options[CONTINUOUS] == ContinuousOps.STANDARDIZATION:
                continue
            # Atributo continuo y estrategia de intervalos variables
            elif attributeType == AttributeType.CONTINUOUS and options[CONTINUOUS] == ContinuousOps.VARIABLE:
                value = dataset.at[index, attributeKey]
                intervals = list(classificator[result][attributeKey].keys())
                interval = processor.getIntervalForValue(value, intervals)
                classificator[result][attributeKey][interval] += 1 
            # Atributo es discreto
            else:   
                value = dataset.at[index, attributeKey]
                classificator[result][attributeKey][value] += 1      
    
    # Se calculan las probabilidades en base a los resultados del dataset.
    for result in results:
        for attributeKey, attributeType in attributes:
            for value in classificator[result][attributeKey]:
                if value != 'mean' and value != 'std':
                    # Para cada resultado se guarda la proporcion de cada valor para cada atributo que clasificó con dicho resultado
                    classificator[result][attributeKey][value] += mEst/len(classificator[result][attributeKey])
                    classificator[result][attributeKey][value] /= amountClass[result] + mEst
    
    return classificator

def nbClassify(classificator, example, attributes, options):
    continuousAttributes = []
    for attributeKey, attributeType in attributes:
        if attributeType == AttributeType.CONTINUOUS:
            continuousAttributes.append(attributeKey)

    probabilitiesResult = {}
    for result in classificator:
        probabilitiesResult[result] = classificator[result]['total']
    
    for result in classificator:
        for key, value in example.items():
            if key != 'class':
                if key in continuousAttributes and options[CONTINUOUS] == ContinuousOps.STANDARDIZATION:
                    probabilitiesResult[result] *= gaussianNormal(float(value), classificator[result][key]['mean'], classificator[result][key]['std'])
                elif key in continuousAttributes and options[CONTINUOUS] == ContinuousOps.VARIABLE:
                    intervals = list(classificator[result][key].keys())
                    interval = processor.getIntervalForValue(value, intervals)
                    probabilitiesResult[result] *= classificator[result][key][interval]
                else:
                    probabilitiesResult[result] *= classificator[result][key][value]

    bestProbability = max(probabilitiesResult.values())

    # En caso de empate al clasificar junta todos los posibles resultados.
    bestResults = [(i,j) for i,j in probabilitiesResult.items() if j == bestProbability]
    return random.choice(bestResults)

### METODOS AUXILIARES
### -------------------

def calculateMean(valuesOfResult, attribute):
    return np.mean(valuesOfResult[attribute], axis=0)

def calculateStandardDeviation(valuesOfResult, attribute):
    return np.std(valuesOfResult[attribute], axis=0)

def gaussianNormal(value, mean, std):
    return 1 if std == 0 else math.exp(-((value-mean)/(2*std))**2)/(math.sqrt(2*math.pi*std**2))
