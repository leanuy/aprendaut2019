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
                self.weights[i] = self.normalize(self.weights[i], 0, 1)

    
    def normalize(self, value, minimum_value, maximum_value):
        if maximum_value - minimum_value > 0:
            return (value - minimum_value)/(maximum_value - minimum_value)
        else:
            return 0