### DEPENDENCIAS
### ------------------

import math

from .node import Node

import processing.calculator as calculator
from utils.const import AttributeType, ContinuousOps, MeasureType

### METODOS PRINCIPALES
### -------------------

def id3Train(dataset, attributes, results, continuous, measureType):

    # Caso Borde: Todos los ejemplos son de una clase
    (result, proportion) = calculator.getMostLikelyResult(dataset, results)
    if proportion == 1:
        return (result, proportion)

    # Caso Borde: No hay más atributos a evaluar
    elif len(attributes) == 0:
        return (result, proportion)

    # No hay caso borde
    else:

        # 1. Obtener atributo con mayor ganancia de información y sus posibles valores
        (attribute, values) = calculator.getBestAttribute(dataset, attributes, results, continuous, measureType)
        (attributeKey, attributeType) = attribute

        # 2. Generar lista de atributos nueva y diccionario de hijos
        newAttributes = list(attributes)
        newAttributes.remove(attribute)
        options = {}

        # 3. Iterar por cada posible valor para el atributo elegido
        for value in values:

            # 3.1. Obtener el subconjunto de ejemplos para el valor 'value' del atributo 'attribute'
            examplesForValue = calculator.getExamplesForValue(dataset, attribute, values, value)

            # 3.2. Si no hay ejemplos, devolver hoja con el resultado más frecuente (y su probabilidad)
            if len(examplesForValue) == 0:
                options[value] = calculator.getMostLikelyResult(dataset, results)

            # 3.3. Si hay ejemplos, devolver rama generada recursivamente
            else:
                options[value] = id3Train(examplesForValue, newAttributes, results, continuous, measureType)

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
                    break
    else:
        return tree
    