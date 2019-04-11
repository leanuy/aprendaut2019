### DEPENDENCIAS
### ------------------
import math
import random
import numpy as np
import processing.processor as processor
import processing.calculator as calculator
from utils.const import AttributeType, ContinuousOps, MeasureOps, CONTINUOUS, MEASURE

### METODOS PRINCIPALES
### -------------------

def nbTrain(dataset, attributes, results, options, m_est = 10):
  # Initialization
  classificator = {}
  amountClass = {}
  proportions = processor.getAllProportionExamplesForResults(dataset, results)
  for result in results:
    classificator[result] = {}
    amountClass[result] = proportions[result] * len(dataset.index)

    # En total se guarda la probabilidad sin considerar atributos.
    classificator[result]['total'] = proportions[result]

    for attribute in attributes:
      (attributeKey, attributeType) = attribute
      classificator[result][attributeKey] = {}
      for value in processor.getPossibleValues(dataset, attribute):
        classificator[result][attributeKey][value] = 0

  # Para los atributos continuos Bayes sencillo asume distribución normal y calcula su esperanza y desviación estándar.
  if options[CONTINUOUS] == ContinuousOps.STANDARDIZATION:
    for attribute in attributes:
      (attributeKey, attributeType) = attribute
      if attributeType == AttributeType.CONTINUOUS:
        for result in results:
          valuesOfResult = dataset[dataset['class'] == result] # Condition: dataset['class'] == result
          classificator[result][attributeKey]['mean'] = calculateMean(valuesOfResult, attributeKey)
          classificator[result][attributeKey]['std_dev'] = calculateStandardDeviation(valuesOfResult, attributeKey)

  # Para cada valor de cada atributo se cuenta la ocurrencia de valores.
  for index in dataset.index:
    result = dataset.at[index, 'class']
    for attribute in attributes:
      (attributeKey, attributeType) = attribute
      value = dataset.at[index, attributeKey]
      classificator[result][attributeKey][value] += 1      
  
  # Se calculan las probabilidades en base a los resultados del dataset.
  for result in results:
    for attribute in attributes:
      (attributeKey, attributeType) = attribute
      for value in classificator[result][attributeKey]:
        if value != 'mean' and value != 'std_dev':
          # Para cada resultado se guarda la proporcion de cada valor para cada atributo que clasificó con dicho resultado
          classificator[result][attributeKey][value] = (classificator[result][attributeKey][value] + m_est/len(classificator[result][attributeKey])) / (amountClass[result] + m_est)
  return classificator

def nbClassify(classificator, example, attributes):
  continuousAttributes = []
  for attribute in attributes:
    (attributeKey, attributeType) = attribute
    if attributeType == AttributeType.CONTINUOUS:
      continuousAttributes.append(attributeKey)

  probabilitiesResult = {}
  for result in classificator:
    probabilitiesResult[result] = classificator[result]['total']
  
  for result in classificator:
    for key, value in example.items():
      if key != 'class':
        if key in continuousAttributes:
          probabilitiesResult[result] *= gaussianNormal(float(value), classificator[result][key]['mean'], classificator[result][key]['std_dev'])
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

def gaussianNormal(value, mean, std_dev):
  return math.exp(-((value-mean)/(2*std_dev))**2)/(math.sqrt(2*math.pi*std_dev**2))
