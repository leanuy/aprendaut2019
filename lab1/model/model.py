### DEPENDENCIAS
### ------------------

import random

### CLASE PRINCIPAL
### ------------------

class Model():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, initialWeights = [0.9, 0.9, 0.9]):
        self.weights = initialWeights

	### GETTERS y SETTERS
    ### -------------------

    def getWeights(self):
    	return self.weights

	### METODOS PRINCIPALES
    ### -------------------

    # Evalua un tablero dado
    def evaluate(self, board):
    	return random.uniform(0, 1)

    # Actualiza los pesos
    def update(self, example):
    	print("Actualizando pesos en base a un tablero y su clasificacion")