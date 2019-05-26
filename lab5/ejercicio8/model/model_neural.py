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
        self.model = MLPRegressor(hidden_layer_sizes=(50,50,50), max_iter=1000, solver='sgd', warm_start=True)
        
        # Setteo el estado inicial del board
        (qValues, features) = self.getBeginningState(options['modelType'])
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
    def update(self, examplesFeatures, examplesEvaluations):
        if self.options['modelType'] == ModelTypes.NEURAL_BOARD:
            for features in examplesFeatures:
                features[features == 2] = -1
        self.model.fit(list(examplesFeatures), examplesEvaluations.ravel())

    def getBeginningState(self, modelType):
        qValue = [0]
        if modelType == ModelTypes.NEURAL_BOARD:
            features = [[
                0,0,0,0,0,1,1,1,1,
                0,0,0,0,0,0,1,1,1,
                0,0,0,0,0,0,0,1,1,
                0,0,0,0,0,0,0,0,1,
                0,0,0,0,0,0,0,0,0,
                -1,0,0,0,0,0,0,0,0,
                -1,-1,0,0,0,0,0,0,0,
                -1,-1,-1,0,0,0,0,0,0,
                -1,-1,-1,-1,0,0,0,0,0
            ]]
        elif modelType == ModelTypes.NEURAL_METRICS:
            features = [[
                0.00026068291113050653,0.49998982354831156,0.49998982354831156,0.0007820487333915196,
                0.0007820487333915196,0.0041709265780881044,0.004692292400349117,0.49998982354831156,0.49998982354831156
            ]]
        return (np.array(qValue), np.array(features))