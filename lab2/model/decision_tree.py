### DEPENDENCIAS
### ------------------

import math
import copy
import pandas as pd

from .node import Node

import processing.calculator as calculator
from processing.processor import Processor
from utils.const import AttributeType, ContinuousOps, MeasureType

### METODOS PRINCIPALES
### -------------------

def id3Train(processor):

    # 0. Recorrer dataset y generar datos necesarios
    processor.processNode()

    print('-', end="")

    # Caso Borde: Todos los ejemplos son de una clase o no hay atributos a evaluar
    if processor.isMostLikelyResult():
        #print("Es hoja, nivel " + str(lvl))
        #print(processor.getMostLikelyResult())
        #print()
        return processor.getMostLikelyResult()

    # Caso Normal    
    else:

        # 1. Obtener atributo con mayor ganancia de información y sus posibles valores
        (attribute, values) = processor.getBestAttribute()
        (attributeKey, attributeType) = attribute

        # 2. Generar diccionario de hijos
        newAttributes = processor.getNewAttributes((attributeKey, attributeType))
        options = {}

        #print("Es rama, nivel " + str(lvl))
        #print("Mejor atributo: " + str(attribute))
        #print("Intervalos: " + str(processor.getIntervals()))
        #print("Valores: " + str(values))
        #print("Nuevos atributos: " + str(newAttributes))
        #print()

        # 3. Iterar por cada posible valor para el atributo elegido 
        for value in values:

            # 3.1. Obtener el subconjunto de ejemplos para el valor 'value' del atributo 'attribute'
            examplesForValue = processor.getExamplesForValue(attributeKey, value)

            # 3.2. Si no hay ejemplos, devolver hoja con el resultado más frecuente (y su probabilidad)
            if len(examplesForValue) == 0:
                options[value] = processor.getMostLikelyResult()

            # 3.3. Si hay ejemplos, devolver rama generada recursivamente
            else:
                newProcessor = copy.deepcopy(processor)
                newProcessor.setDataset((examplesForValue, pd.DataFrame(examplesForValue)))
                newProcessor.setNewAttributes(newAttributes)
                options[value] = id3Train(newProcessor)

        # 4. Devolver nodo intermedio
        return Node(attribute, options)

def id3Classify(tree, example):
    if type(tree) == Node:
        currentAttribute = tree.attribute
        currentAttributeType = tree.attributeType
        currentBranches = list(tree.options.keys())
        for branch in currentBranches:
            if currentAttributeType == AttributeType.DISCRETE:
                if branch == example[currentAttribute]:
                    node = tree.options[branch]
                    if type(node) == Node:
                        return id3Classify(node, example)
                    else:
                        return node
            else:
                value = example[currentAttribute]
                if branch == 'bigger' or value <= branch:
                    node = tree.options[branch]
                    if type(node) == Node:
                        return id3Classify(node, example)
                    else:
                        return node
    else:
        return tree
    
