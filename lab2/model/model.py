### DEPENDENCIAS
### ------------------

import numpy as np
import random

from .decision_tree import id3Train, id3Classify
from .decision_forest import id3ForestTrain, id3ForestClassify

from processing.processor import Processor

from utils.const import ModelOps, ContinuousOps, MeasureType

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
        return self.model

    def getDataset(self):
        return self.dataset

    def getModelAttributes(self):
        return self.attributes

    def getModelAttributesNames(self):
        attributeNames = []
        for attribute in self.attributes:
            (attributeKey, attributeValue) = attribute
            attributeNames.append(attributeKey)
        return attributeNames

    def getModelResults(self):
        return self.results

    def getClassifier(self):
        return self.classifier

    ### METODOS PRINCIPALES
    ### -------------------

    def train(self, dataset, attributes, results, continuous = 0, measureType = MeasureType.GAIN):

        (self.dataset, self.df) = dataset 
        self.attributes = attributes
        self.results = results

        if self.model == ModelOps.DECISION_TREE:
            self.classifier = self.trainTree(continuous, measureType)

        elif self.model == ModelOps.DECISION_FOREST:
            self.classifier = self.trainForest(continuous, measureType)

    def classify(self, example):

        if self.model == ModelOps.DECISION_TREE:
            return self.classifyTree(example)

        elif self.model == ModelOps.DECISION_FOREST:
            return self.classifyForest(example)

    ### METODOS AUXILIARES
    ### -------------------

    def classifySet(self, exampleSet):
        
        results = []
        
        for example in exampleSet:
            example['class'] = self.classify(example)
            results.append(example)

        return results

    def printClassifier(self):

        if self.model == ModelOps.DECISION_TREE:
            self.classifier.printTree(0)
            print()

        elif self.model == ModelOps.DECISION_FOREST:
            for result in self.classifier:
                print("Árbol para clase " + str(result))
                print()
                self.classifier[result].printTree(0)
                print()

    ### METODOS INTERNOS
    ### -------------------

    def trainTree(self, continuous, measure):
        return id3Train(Processor((self.dataset, self.df), self.attributes, self.results, self.attributes, continuous, measure, len(self.dataset)), 0)

    def classifyTree(self, example):
        return id3Classify(self.classifier, example)

    def trainForest(self, continuous, measure):
        return id3ForestTrain(Processor((self.dataset, self.df), self.attributes, self.results, self.attributes, continuous, measure, len(self.dataset)))

    def classifyForest(self, example):
        return id3ForestClassify(self.classifier, example, self.results)

