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
    def update(self, board, v_t, k):
        # LMS weight update rule
        v_t_tablero = self.evaluate(board)
		X = board.get_features()
		for i in range(len(self.weights)):
            self.weights[i] = self.weights[i] + k * (v_t - v_t_tablero) * X[i]

    	print("Actualizando pesos en base a un tablero y su clasificacion")