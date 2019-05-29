### DEPENDENCIAS
### ------------------

from sklearn.neural_network import MLPRegressor
from scipy import sparse

import numpy as np
import random

import processing.reader as reader

from utils.const import InputLayerTypes, GameTokens, DATA_BOARDS, DATA_METRICS

### CLASE PRINCIPAL
### ------------------

class ModelNeural():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, options, playerToken):
        self.options = options
        self.model = MLPRegressor(solver='sgd', warm_start=True, max_iter=1000,
                                  hidden_layer_sizes=(options['hiddenLayerSizes']), activation=options['activationFunction'].value,
                                  learning_rate=options['learningRate'][0], learning_rate_init=options['learningRate'][1])
        
        # Setteo el estado inicial del board
        (qValues, features) = self.getBeginningState(options['inputLayer'])
        self.model.fit(features, qValues.ravel())


    ### METODOS PRINCIPALES
    ### -------------------

    # Evalua un tablero en forma de features
    def evaluate(self, features):
        if self.options['inputLayer'] == InputLayerTypes.BOARD:
            features = [-1 if x==2 else x for x in features]
        return self.model.predict(np.array([features]))

    # Actualiza los pesos del modelo siguiendo LMS
    def update(self, examplesFeatures, examplesEvaluations):
        if self.options['inputLayer'] == InputLayerTypes.BOARD:
            for features in examplesFeatures:
                features[features == 2] = -1
        self.model.fit(list(examplesFeatures), examplesEvaluations.ravel())

    ### METODOS AUXILIARES
    ### -------------------

    def getBeginningState(self, modelType):
        qValue = [0]
        if modelType == InputLayerTypes.BOARD:
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
        elif modelType == InputLayerTypes.METRICS:
            features = [[
                0.00026068291113050653,0.49998982354831156,0.49998982354831156,0.0007820487333915196,
                0.0007820487333915196,0.0041709265780881044,0.004692292400349117,0.49998982354831156,0.49998982354831156
            ]]
        return (np.array(qValue), np.array(features))