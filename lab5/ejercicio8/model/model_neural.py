### DEPENDENCIAS
### ------------------

from sklearn.neural_network import MLPRegressor
from scipy import sparse

import numpy as np
import random

import processing.reader as reader

from utils.const import ModelTypes, GameTokens, DATA_BOARDS, DATA_METRICS

### CLASE PRINCIPAL
### ------------------

class ModelNeural():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, options, playerToken):
        self.options = options
        self.model = MLPRegressor(hidden_layer_sizes=(30,30,30), max_iter=1000)
        
        # Setteo de los estados básicos del board
        if options['modelType'] == ModelTypes.NEURAL_BOARD:
            (qValues, features) = reader.readDatasetBoard(DATA_BOARDS)
        elif options['modelType'] == ModelTypes.NEURAL_METRICS:
            (qValues, features) = reader.readDatasetMetrics(DATA_METRICS)

        # TODO: Investigar por qué player 2 anda bien solo con los Q-Values de player 1...
        #if playerToken == GameTokens.PLAYER2:
        #    qValues = (-1)*qValues
        
        self.model.fit(features, qValues.ravel())

    ### GETTERS y SETTERS
    ### -------------------


    ### METODOS PRINCIPALES
    ### -------------------

    # Evalua un tablero en forma de features
    def evaluate(self, features):
        if self.options['modelType'] == ModelTypes.NEURAL_BOARD:
            features = [-1 if x==2 else x for x in features]
        return self.model.predict(np.array([features]))

    # Actualiza los pesos del modelo siguiendo LMS
    def update(self, features, trainingEvaluation, learningRate):
        currentEvaluation = self.evaluate(features)
        if self.options['modelType'] == ModelTypes.NEURAL_BOARD:
            features = [-1 if x==2 else x for x in features]
        self.model.fit(np.array([features]), np.array([learningRate * (trainingEvaluation - currentEvaluation)]).ravel())
        return trainingEvaluation - currentEvaluation
        