### DEPENDENCIAS
### ------------------

import math

from .node import Node

import processing.reader as reader
from utils.const import AttributeType, ContinuousOps

### METODOS PRINCIPALES
### -------------------

def id3Train(dataset, attributes, results, continuous):

    # Caso Borde: Todos los ejemplos son de una clase
    (result, proportion) = reader.getMostLikelyResult(dataset, results)
    if proportion == 1:
        return (result, proportion)

    # Caso Borde: No hay más atributos a evaluar
    elif len(attributes) == 0:
        return (result, proportion)

    # No hay caso borde
    else:

        # 1. Obtener atributo con mayor ganancia de información y sus posibles valores
        (attribute, values) = getBestAttribute(dataset, attributes, results, continuous)
        (attributeKey, attributeType) = attribute

        # 2. Generar lista de atributos nueva y diccionario de hijos
        newAttributes = list(attributes)
        newAttributes.remove(attribute)
        options = {}

        print("Atributo elegido: " + str(attributeKey))
        print("Posibles valores: " + str(values))
        print("Atributos restantes: " + str(newAttributes))
        print()

        # 4. Iterar por cada posible valor para el atributo elegido
        for value in values:

            # 4.1. Obtener el subconjunto de ejemplos para el valor 'value' del atributo 'attribute'
            examplesForValue = reader.getExamplesForValue(dataset, attribute, value)

            print("Atributo elegido: " + str(attributeKey))
            print("Valor elegido: " + str(value))
            print("Dataset: " + str(examplesForValue))
            print()

            # 4.2. Si no hay ejemplos, devolver hoja con el resultado más frecuente (y su probabilidad)
            if len(examplesForValue) == 0:
                options[value] = reader.getMostLikelyResult(dataset, results)

            # 4.3. Si hay ejemplos, devolver rama generada recursivamente
            else:
                options[value] = id3Train(examplesForValue, newAttributes, results, continuous)

        # 5. Devolver nodo intermedio
        return Node(attribute, options)

def id3Classify(tree, example, continuous):
    if type(tree) == Node:
        currentAttribute = tree.attribute
        currentAttributeType = tree.attributeType
        currentBranches = list(tree.options.keys())
        for branch in currentBranches:
            if currentAttributeType == AttributeType.DISCRETE:
                if branch == example[currentAttribute]:
                    node = tree.options[branch]
                    if type(node) == Node:
                        return id3Classify(node, example, continuous)
                    else:
                        return node
            else:
                value = example[currentAttribute]
                if branch == 'bigger' or value <= branch:
                    node = tree.options[branch]
                    if type(node) == Node:
                        return id3Classify(node, example, continuous)
                    else:
                        return node
                    break
    else:
        return tree
    
### METODOS AUXILIARES
### -------------------

# A
def getBestAttribute(dataset, attributes, results, continuous):
  
    (bestAttribute, bestAttributeType) = attributes[0]
    bestValues = reader.getDiscretePossibleValues(dataset, attributes[0], continuous)

    for attribute in attributes[1:]:
        (attributeKey, attributeType) = attribute
        possibleValues = reader.getDiscretePossibleValues(dataset, attribute, continuous)
        if getGain(dataset, attribute, possibleValues, results) > getGain(dataset, (bestAttribute, bestAttributeType), bestValues, results):
            bestAttribute = attributeKey
            bestAttributeType = attributeType
            bestValues = possibleValues

    return ((bestAttribute, bestAttributeType), bestValues)

# A
def getGain(dataset, attribute, possibleValues, results):
    
    entropy = 0
    for value in possibleValues:
        subset = reader.getExamplesForValue(dataset, attribute, value)
        entropy += ((len(subset)/len(dataset)) * getEntropy(subset, results))

    return (getEntropy(dataset, results) - entropy)

# A
def getEntropy(dataset, results):

    proportions = []
    for result in results:
      proportions.append(reader.proportionExamplesForResult(dataset, result))

    entropy = 0
    for p in proportions:
      if p != 0:
        entropy += -p * math.log(p,2)

    return entropy