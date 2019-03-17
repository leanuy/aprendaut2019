### DEPENDENCIAS
### ------------------

import numpy as np
import random

### CLASE PRINCIPAL
### ------------------

class Model():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, normalize_weights, initialWeights = [0.9, 0.9, 0.9, 0.9, 0.9]):
        self.weights = initialWeights
        self.normalize_weights = normalize_weights

    ### GETTERS y SETTERS
    ### -------------------

    def getWeights(self):
        return self.weights

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

    
    def normalize(self, values):
        maximum_value = max(values)
        minimum_value = min(values)
        for value in values:
            if maximum_value - minimum_value > 0:
                value = (value - minimum_value)/(maximum_value - minimum_value) 
            else:
                value = 0
        return values
        