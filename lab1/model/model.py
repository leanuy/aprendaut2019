### DEPENDENCIAS
### ------------------

import random

### CLASE PRINCIPAL
### ------------------

class Model():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, initialWeights = [0.9, 0.9, 0.9, 0.9]):
        self.weights = initialWeights

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