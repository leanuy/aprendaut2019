### DEPENDENCIAS
### ------------------
import math
import random
import processing.processor as processor
import processing.calculator as calculator
from utils.const import AttributeType, ContinuousOps, MeasureOps, CONTINUOUS, MEASURE

### METODOS PRINCIPALES
### -------------------

def nbTrain(dataset, attributes, results, options, m_est = 1):
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

  # Para los atributos continuos Bayes sencillo asume distribución normal y calcula su esperanza y varianza.
  # The other option is options[CONTINUOUS] == ContinuousOps.VARIABLE:
  if options[CONTINUOUS] == ContinuousOps.STANDARDIZATION:
    for attribute in attributes:
      (attributeKey, attributeType) = attribute
      if attributeType == AttributeType.CONTINUOUS:
        for result in results:
          valuesOfResult = dataset[dataset['class'] == result] # Condition: dataset['class'] == result
          mean = calculate_mean(valuesOfResult, attributeKey, result)
          classificator[result][attributeKey]['mean'] = mean
          classificator[result][attributeKey]['variance'] = calculate_variance(valuesOfResult, attributeKey, mean, result)

  # Para cada valor de cada atributo se cuenta la ocurrencia de valores.
  for index in dataset.index:
    result = dataset.at[index, 'class']
    for attribute in attributes:
      (attributeKey, attributeType) = attribute
      value = dataset.at[index, attributeKey]
      classificator[result][attributeKey][value] += 1      
  
  # Se calculan las probabilidades en base a los resultados del dataset.
  for result in results:
    for key, values in classificator[result].items():
      if key != 'total': # key = AttributeKey
        # Para cada resultado se guarda la proporcion de cada valor para cada atributo que clasificó con dicho resultado
        for value, count in values.items():
          classificator[result][key][value] = (classificator[result][key][value] + m_est/len(classificator[result][key])) / (amountClass[result] + m_est)

  return classificator

def nbClassify(classificator, example, attributes):
  continuousAttributes = []
  for attribute in attributes:
    (attributeKey, attributeType) = attribute
    if attributeType == AttributeType.CONTINUOUS:
      continuousAttributes.append(attributeKey)

  probabilitiesResult = {}
  for result, attributeDict in classificator.items():
    probabilitiesResult[result] = classificator[result]['total']
  
  for key, value in example.items():
    if key != 'class':
      if key in continuousAttributes:
        probabilitiesResult[result] *= gaussian_normal(float(value), classificator[result][key]['mean'], classificator[result][key]['variance'])
      else:
        probabilitiesResult[result] *= classificator[result][key][value]

  bestProbability = max(probabilitiesResult.values())
  # print(probabilitiesResult)
  # print(bestProbability)
  # En caso de empate al clasificar junta todos los posibles resultados.
  bestResults = [(i,j) for i,j in probabilitiesResult.items() if j == bestProbability]
  return random.choice(bestResults)

### METODOS AUXILIARES
### -------------------

def calculate_mean(valuesOfResult, attribute, result):
  values = [x/len(valuesOfResult) for x in valuesOfResult[attribute]]
  return sum(values)

def calculate_variance(valuesOfResult, attribute, mean, result):
  values = [(x - mean) ** 2 for x in valuesOfResult[attribute]]
  return math.sqrt(sum(values)/(len(values) - 1))

def gaussian_normal(value, mean, variance):
  return math.exp(-((value-mean)/(2*variance))**2)/(math.sqrt(2*math.pi*variance**2))
