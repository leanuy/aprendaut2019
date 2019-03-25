### DEPENDENCIAS
### ------------------

import numpy as np
import random

from .decision_tree import id3Train, id3Classify
from .decision_forest import id3ForestTrain, id3ForestClassify

import processing.reader as reader

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
        self.results = None
        self.classifier = None

    ### GETTERS y SETTERS
    ### -------------------

    def getModelType(self):
        return self.modelType

    def getModelAttributes(self):
        return self.attributes

    def getClassifier(self):
        return self.classifier

    ### METODOS PRINCIPALES
    ### -------------------

    def train(self, dataset, continuous = 0):

        self.dataset = dataset
        self.attributes = reader.getAttributes(dataset)
        self.results = reader.getResults(dataset)

        print(self.attributes)
        print(self.results)
        
        if self.model == ModelOps.DECISION_TREE:
            self.classifier = self.trainTree(continuous)

        elif self.model == ModelOps.DECISION_FOREST:
            self.classifier = self.trainForest(continuous)

    def classify(self, example, continuous = 0):

        if self.model == ModelOps.DECISION_TREE:
            return self.classifyTree(example, continuous)

        elif self.model == ModelOps.DECISION_FOREST:
            return self.classifyForest(example, continuous)

    ### METODOS AUXILIARES
    ### -------------------

    def classifySet(self, example_set, continuous = 0):
        
        results = []
        
        for example in example_set:
            res = self.classify(example, continuous)
            results.append(res)

        return results

    def printClassifier(self):
        self.classifier.printTree(0)
        print()

    ### METODOS INTERNOS
    ### -------------------

    def trainTree(self, continuous):
        return id3Train(self.dataset, self.attributes, self.results, continuous)

    def classifyTree(self, example, continuous):
        return id3Classify(self.classifier, example, continuous)

    def trainForest(self, continuous):
        return id3ForestTrain(self.dataset, self.attributes, self.results, continuous)

    def classifyForest(self, example, continuous):
        return id3ForestClassify(self.classifier, example, continuous)

