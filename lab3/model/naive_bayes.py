### DEPENDENCIAS
### ------------------
import math
import processing.processor as processor
import processing.calculator as calculator
from utils.const import AttributeType, ContinuousOps, MeasureOps, CONTINUOUS, MEASURE

### METODOS PRINCIPALES
### -------------------

def nbTrain(dataset, attributes, results, options):
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
          mean = calculate_mean(dataset, attributeKey, result)
          classificator[result][attributeKey]['mean'] = mean
          classificator[result][attributeKey]['variance'] = calculate_variance(dataset, attributeKey, mean, result)

  # Para cada valor de cada atributo se cuenta la ocurrencia de valores.
  for index in dataset.index:
    for attribute in attributes:
      (attributeKey, attributeType) = attribute
      for value in processor.getPossibleValues(dataset, attribute):
        result = dataset.at[index,'class']
        classificator[result][attributeKey][value] += 1
  
  # Se calculan las probabilidades en base a los resultados del dataset.
  for result in results:
    for key, values in classificator[result]:
      if key != 'total':
        # key = AttributeKey
        # En cada 
        for value, count in values.items():
          classificator[result][key][value] = (classificator[result][key][value] + m_est/len(classificator[result][key])) / (amountClass[result] + m_est)

  return classificator

def nbClassify(forest, example, results):
  return False

### METODOS AUXILIARES
### -------------------

def calculate_mean(dataset, attribute, result):
  values_used = dataset[dataset['class'] == result] # Condition: dataset['class'] == result
  values = [x[attribute]/len(values_used) for x in values_used]
  return sum(values)

def calculate_variance(dataset, attribute, mean, result):
  values = [(x[attribute] - mean) ** 2 for x in dataset if x['class'] == result]
  return math.sqrt(sum(values)/(len(values) - 1))

def gaussian_normal(value, mean, variance):
  return math.exp(-((value-mean)/(2*variance))**2)/(math.sqrt(2*math.pi*variance**2))
