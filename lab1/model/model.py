### DEPENDENCIAS
### ------------------

import random

### CLASE PRINCIPAL
### ------------------

class Model():

    ### METODOS PRINCIPALES
    ### -------------------

    def __init__(self, initialWeights = [0.9, 0.9, 0.9]):
        self.weights = initialWeights

    # Evalua un tablero dado
    def evaluate(self, board):
    	print("Evaluando un tablero en base a los pesos actuales")
    	return random.uniform(0, 1)


    # Actualiza los pesos
    def update(self, example):
    	print("Actualizando pesos en base a un tablero y su clasificacion")
