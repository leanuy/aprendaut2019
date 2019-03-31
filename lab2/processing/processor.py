### DEPENDENCIAS
### ------------------

import copy

from . import parser
from . import calculator

from utils.const import AttributeType, ContinuousOps

### CLASE PRINCIPAL
### ------------------

class Processor():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, dataset, attributes, results, newAttributes, continuous, measure, datasetLength):
        (self.dataset, self.df) = dataset
        self.attributes = attributes
        self.results = results
        self.newAttributes = newAttributes
  
        self.continuous = continuous
        self.measure = measure

        self.datasetLength = 0
        self.isBorderCase = False
        self.mostLikelyResult = None

        self.intervals = {}
        self.examplesForValue = {}
        self.proportionsForValue = {}
        self.proportionsForResult = {}

    ### GETTERS & SETTERS
    ### -------------------

    def getAttributes(self):
        return self.attributes

    def getResults(self):
        return self.results

    def getContinuous(self):
        return self.continuous

    def getMeasure(self):
        return self.measure

    def getDatasetLength(self):
        return self.datasetLength

    def setDataset(self, dataset):
        (self.dataset, self.df) = dataset

    def setNewAttributes(self, newAttributes):
        self.newAttributes = newAttributes

    def getIntervals(self):
        return self.intervals

    ### METODOS PRINCIPALES
    ### -------------------

    def processNode(self):

        # Reiniciar todo
        self.datasetLength = len(self.dataset)
        self.intervals = {}
        self.examplesForValue = {}
        self.proportionsForValue = {}
        self.proportionsForResult = {}

        # Comprobar si es caso borde (ya no hay atributos)
        if len(self.newAttributes) == 0 or self.datasetLength <= 1:
            self.isBorderCase = True
        
        # Recorrer cada atributo
        for attributeKey, attributeType in self.attributes:

            # Para generar diccionario de posibles valores para un atributo
            self.examplesForValue[attributeKey] = {}
            self.proportionsForValue[attributeKey] = {}

            if attributeType == AttributeType.CONTINUOUS:

                values = self.df[[attributeKey,'class']].sort_values(attributeKey)

                if self.continuous == ContinuousOps.FIXED:

                    median = len(values) // 2

                    self.intervals[attributeKey] = []
                    self.intervals[attributeKey].append(values[attributeKey][median])
                    self.intervals[attributeKey].append("bigger")

                elif self.continuous == ContinuousOps.VARIABLE:

                    self.intervals[attributeKey] = []
                    lastRes = None
                    lastExample = None

                    for index, value in values.iterrows():
                        if lastRes != None and value['class'] != lastRes:
                            self.intervals[attributeKey].append(((float(value[attributeKey]) - float(lastExample)) / 2) + float(lastExample))
                        lastRes = value['class']
                        lastExample = value[attributeKey]
                    self.intervals[attributeKey].append("bigger")

        # Recorrer cada ejemplo del dataset
        for example in self.dataset:

            # Obtener clasificación en 'example'
            result = example['class']
            
            # Para generar diccionario de proporciones para cada resultado
            # Si no existe: Generar proporción
            # Si existe: Sumar 1 a proporción
            if result not in self.proportionsForResult:
                self.proportionsForResult[result] = 0
            self.proportionsForResult[result] += 1

            if not self.isBorderCase:
              
                # Recorrer cada entrada del ejemplo
                for attributeKey, attributeType in self.attributes:

                    # Obtener valor para 'attribute' en 'example'
                    rawValue = example[attributeKey]

                    # Obtener valor procesado
                    if attributeType == AttributeType.DISCRETE:
                        value = rawValue
                    else:
                        value = parser.getDiscreteValue(self.intervals[attributeKey], rawValue)

                    # Para generar subsets de ejemplos por valor de un atributo
                    # Si no existe: Generar lista de ejemplos para 'attribute'='value'
                    # Si existe: Agregar 'example' a la lista para 'attribute'='value'
                    if value not in self.examplesForValue[attributeKey]:
                        self.examplesForValue[attributeKey][value] = []
                    self.examplesForValue[attributeKey][value].append(example)

                    if value not in self.proportionsForValue[attributeKey]:
                        self.proportionsForValue[attributeKey][value] = {}
                    if result not in self.proportionsForValue[attributeKey][value]:
                        self.proportionsForValue[attributeKey][value][result] = 0
                    self.proportionsForValue[attributeKey][value][result] += 1

        # Recorrer cada subconjunto y sus proporciones 
        for attribute in self.proportionsForValue:
            for value in self.proportionsForValue[attribute]:
                for result in self.proportionsForValue[attribute][value]:
                    self.proportionsForValue[attribute][value][result] /= len(self.examplesForValue[attribute][value])

        # Recorrer cada resultado y sus proporciones 
        for result in self.proportionsForResult:
            # Dividir conteo sobre largo del dataset para obtener proporción
            self.proportionsForResult[result] /= self.datasetLength

        # Recorrer cada resultado y sus proporciones 
        for result in self.proportionsForResult:

            # Comprobar si la clasificación es 1, lo cual implica un caso borde
            if self.proportionsForResult[result] == 1:
                self.isBorderCase = True
                self.mostLikelyResult = (result, self.proportionsForResult[result])
                break

            # Si no, obtener clasificación más probable
            else:
              if self.mostLikelyResult == None:
                  self.mostLikelyResult = (result, self.proportionsForResult[result])
              else:
                  (bestResult, proportion) = self.mostLikelyResult
                  if proportion < self.proportionsForResult[result]:
                      self.mostLikelyResult = (result, self.proportionsForResult[result])

    ### METODOS AUXILIARES - ATRIBUTOS
    ### --------------------------------

    def getBestAttribute(self):
        return calculator.getBestAttribute(self.datasetLength, self.newAttributes, self.examplesForValue, self.proportionsForValue, self.proportionsForResult, self.continuous, self.measure)

    def getNewAttributes(self, attribute):
        newAttributes = copy.deepcopy(self.newAttributes)
        newAttributes.remove(attribute)
        return newAttributes

    ### METODOS AUXILIARES - EJEMPLOS
    ### --------------------------------

    def getExamplesForValue(self, attribute, value):
        return self.examplesForValue[attribute][value]

    ### METODOS AUXILIARES - RESULTADOS
    ### --------------------------------

    def isMostLikelyResult(self):
        return self.isBorderCase

    def getMostLikelyResult(self):
        return self.mostLikelyResult

    