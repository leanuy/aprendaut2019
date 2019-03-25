### DEPENDENCIAS
### ------------------

import math

from .node import Node

import processing.reader as reader

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
        (attribute, possibleValues) = getBestAttribute(dataset, attributes, results, continuous)

        # 2. Generar lista de atributos nueva y diccionario de hijos
        newAttributes = list(attributes)
        newAttributes.remove(attribute)
        options = {}

        # 4. Iterar por cada posible valor para el atributo elegido
        for value in possibleValues:

            # 4.1. Obtener el subconjunto de ejemplos para el valor 'value' del atributo 'attribute'
            examplesForValue = reader.getExamplesForValue(dataset, attribute, possibleValues, value, continuous)

            # 4.2. Si no hay ejemplos, devolver hoja con el resultado más frecuente (y su probabilidad)
            if len(examplesForValue) == 0:
                options[value] = reader.getMostLikelyResult(dataset, results)

            # 4.3. Si hay ejemplos, devolver rama generada recursivamente
            else:
                options[value] = id3Train(examplesForValue, newAttributes, results, continuous)

        # 5. Devolver nodo intermedio
        return Node(attribute, options)

def id3Classify(tree, example, continuous):
    print("Clasificador ID3 Tree")
    return True

### METODOS AUXILIARES
### -------------------

# A
def getBestAttribute(dataset, attributes, results, continuous):
  
    (bestAttribute, bestAttributeType) = attributes[0]
    bestValues = reader.getPossibleValues(dataset, attributes[0], continuous)

    for attribute in attributes[1:]:
        (attributeKey, attributeType) = attribute
        possibleValues = reader.getPossibleValues(dataset, attribute, continuous)
        if getGain(dataset, attribute, possibleValues, results, continuous) > getGain(dataset, (bestAttribute, bestAttributeType), bestValues, results, continuous):
            bestAttribute = attributeKey
            bestAttributeType = attributeType
            bestValues = possibleValues

    return ((bestAttribute, bestAttributeType), bestValues)

# A
def getGain(dataset, attribute, possibleValues, results, continuous):
    
    entropy = 0
    for value in possibleValues:
        subset = reader.getExamplesForValue(dataset, attribute, possibleValues, value, continuous)
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
