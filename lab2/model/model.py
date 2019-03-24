### DEPENDENCIAS
### ------------------

import numpy as np
import random

from .decision_tree import id3_train, id3_classify
from .decision_forest import id3_forest_train, id3_forest_classify

from utils.const import ModelOps, ContinuousOps

### CLASE PRINCIPAL
### ------------------

class Model():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, modelType):
        self.model = modelType
        self.dataset = None
        self.attributes = None
        self.classifier = None

    ### GETTERS y SETTERS
    ### -------------------

    def getModelType(self):
        return self.modelType

    def getAttributes(self):
        return self.attributes

    def getClassifier(self):
        return self.classifier

    ### METODOS PRINCIPALES
    ### -------------------

    def train(self, dataset, continuous = 0):

        self.dataset = dataset
        self.attributes = []

        if self.model == ModelOps.DECISION_TREE:
            self.classifier = self.train_tree(continuous)

        elif self.model == ModelOps.DECISION_FOREST:
            self.classifier = self.train_forest(continuous)

    def classify(self, example, continuous = 0):

        if self.model == ModelOps.DECISION_TREE:
            return self.classify_tree(example, continuous)

        elif self.model == ModelOps.DECISION_FOREST:
            return self.classify_forest(example, continuous)

    ### METODOS AUXILIARES
    ### -------------------

    def classify_set(self, example_set, continuous = 0):
        
        results = []
        
        for example in example_set:
            res = self.classify(example, continuous)
            results.append(res)

        return results

    ### METODOS INTERNOS
    ### -------------------

    def train_tree(self, continuous):
        return id3_train(self.dataset, self.attributes, continuous)

    def classify_tree(self, example, continuous):
        return id3_classify(self.classifier, example, continuous)

