### DEPENDENCIAS
### ------------------

import math

from .node import Node

import processing.reader as reader

### METODOS PRINCIPALES
### -------------------

def id3Train(dataset, attributes, results, continuous, showDecisions):

    # Caso Borde: Todos los ejemplos son de una clase
    (result, proportion) = reader.getMostLikelyResult(dataset, results)
    if proportion == 1:
        return (result, proportion)

    # Caso Borde: No hay más atributos a evaluar
    elif len(attributes) == 0:
        return (result, proportion)

    # No hay caso borde
    else:

        if showDecisions:
            showCurrentDecisions(dataset, attributes, results, continuous)

        # 1. Obtener atributo con mayor ganancia de información y sus posibles valores
        (attribute, possibleValues) = getBestAttribute(dataset, attributes, results, continuous)

        if showDecisions:
            print('-> Mejor Atributo: ', end='')
            print(attribute)
            print()

        # 2. Generar lista de atributos nueva y diccionario de hijos
        newAttributes = list(attributes)
        newAttributes.remove(attribute)
        options = {}

        # 4. Iterar por cada posible valor para el atributo elegido
        for value in possibleValues:

            if showDecisions:
              print('-> Valor: ', end='')
              print(value)
              print()

            # 4.1. Obtener el subconjunto de ejemplos para el valor 'value' del atributo 'attribute'
            examplesForValue = reader.getExamplesForValue(dataset, attribute, possibleValues, value)

            # 4.2. Si no hay ejemplos, devolver hoja con el resultado más frecuente (y su probabilidad)
            if len(examplesForValue) == 0:
                options[value] = reader.getMostLikelyResult(dataset, results)

            # 4.3. Si hay ejemplos, devolver rama generada recursivamente
            else:
                options[value] = id3Train(examplesForValue, newAttributes, results, continuous, showDecisions)

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
        if getGain(dataset, attribute, possibleValues, results) > getGain(dataset, (bestAttribute, bestAttributeType), bestValues, results):
            bestAttribute = attributeKey
            bestAttributeType = attributeType
            bestValues = possibleValues

    return ((bestAttribute, bestAttributeType), bestValues)

# A
def getGain(dataset, attribute, possibleValues, results):
    
    entropy = 0
    for value in possibleValues:
        subset = reader.getExamplesForValue(dataset, attribute, possibleValues, value)
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

### METODOS INTERNOS
### -------------------

# A
def showCurrentDecisions(dataset, attributes, results, continuous):

    for attribute in attributes:
        (attributeKey, attributeType) = attribute
        possibleDiscreteValues = reader.getPossibleDiscreteValues(dataset, attributeKey)

        possibleValues = reader.getPossibleValues(dataset, attribute, continuous)
        proportions = []        
        entropies = []
        totals = []        
        for value in possibleValues:
            subset = reader.getExamplesForValue(dataset, attribute, possibleValues, value)
            proportions.append((len(subset)/len(dataset)))
            entropies.append(getEntropy(subset, results))
            totals.append((len(subset)/len(dataset)) * getEntropy(subset, results))

        attributeGain = getGain(dataset, attribute, possibleValues, results)

        print()
        print('Atributo: ', end='')
        print(attributeKey)
        print('Valores Discretos: ', end='')
        print(possibleDiscreteValues)
        print('Valores: ', end='')
        print(possibleValues)
        print('Proporcion de cada valor: ', end='')
        print(proportions)
        print('Entropia de cada valor: ', end='')
        print(entropies)
        print('Total de cada valor: ', end='')
        print(totals)
        print('Entropia total: ', end='')
        print(getEntropy(dataset, results))
        print('Ganancia: ', end='')
        print(attributeGain)
        
    input()
