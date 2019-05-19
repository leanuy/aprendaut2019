### DEPENDENCIAS
### ------------------

import numpy as np
import random

### CLASE PRINCIPAL
### ------------------

class ModelNeural():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, options):
        self.options = options

    ### GETTERS y SETTERS
    ### -------------------


    ### METODOS PRINCIPALES
    ### -------------------

    # Evalua un tablero en forma de features
    def evaluate(self, features):
        total = 0
        for i in range(len(features)):
            total += features[i]*self.weights[i]
        return total

    # Actualiza los pesos del modelo siguiendo LMS
    def update(self, features, trainingEvaluation, learningRate):
        currentEvaluation = self.evaluate(features)
        for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] + learningRate * (trainingEvaluation - currentEvaluation) * features[i]
        if self.normalize_weights:
            self.weights = self.normalize(self.weights)
        return trainingEvaluation - currentEvaluation
    
    def normalize(self, values):
        normalized_values = []
        maximum_value = max(values)
        minimum_value = min(values)
        for value in values:
            if maximum_value - minimum_value > 0:
                normalized_values.append((value - minimum_value)/(maximum_value - minimum_value))
            else:
                normalized_values.append(0)
        return normalized_values
        