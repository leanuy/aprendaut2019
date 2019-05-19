### DEPENDENCIAS
### ------------------

from sklearn.neural_network import MLPRegressor

import numpy as np
import random

from utils.const import ModelTypes, GameTokens

### CLASE PRINCIPAL
### ------------------

class ModelNeural():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, options, playerToken):
        self.options = options
        self.model = MLPRegressor(hidden_layer_sizes=(10,10,10))
        
        # Setteo de los estados básicos del board
        if options['modelType'] == ModelTypes.NEURAL_BOARD:
            print("TBD")
        elif options['modelType'] == ModelTypes.NEURAL_METRICS:
            player1Win = np.array([[0.00762625879407049, 0.43469675126201796, 0.5567168919671458, 0.03050503517628196, 0.03050503517628196, 0.00762625879407049, 0.01525251758814098, 0.43469675126201796, 0.5567168919671458]])
            beginning = np.array([[0.00026068291113050653, 0.49998982354831156, 0.49998982354831156, 0.0007820487333915196, 0.0007820487333915196, 0.0041709265780881044, 0.004692292400349117, 0.49998982354831156, 0.49998982354831156]])
            player1Loss = np.array([[0.003272292654585248, 0.6839091648083168, 0.20288214458428536, 0.08180731636463119, 0.022906048582096734, 0.04581209716419347, 0.013089170618340992, 0.6839091648083168, 0.11780253556506892]])

        self.model.fit(beginning, [0])

        # FIX: WTF, ESTO POR ALGUNA RAZÓN ANDA MEJOR PONIENDOLE -1 A player1Win CON PLAYER1
        # FIX: La heuristica queda rara igual, se van todos para el costado
        #if playerToken == GameTokens.PLAYER1:
            #self.model.fit(player1Win, [1])
            #self.model.fit(player1Loss, [-1])
        #else:
            #self.model.fit(player1Win, [-1])
            #self.model.fit(player1Loss, [1])

    ### GETTERS y SETTERS
    ### -------------------


    ### METODOS PRINCIPALES
    ### -------------------

    # Evalua un tablero en forma de features
    def evaluate(self, features):
        return self.model.predict(np.array([features]))

    # Actualiza los pesos del modelo siguiendo LMS
    def update(self, features, trainingEvaluation, learningRate):
        currentEvaluation = self.evaluate(features)
        self.model.fit(np.array([features]), [learningRate * (trainingEvaluation - currentEvaluation)])
        return trainingEvaluation - currentEvaluation
    
        