### DEPENDENCIAS
### ------------------

import numpy as np
import random

from .decision_tree import id3Train, id3Classify
from .decision_forest import id3ForestTrain, id3ForestClassify

import processing.reader as reader
import processing.parser as parser

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

    def getDataset(self):
        return self.dataset

    ### METODOS PRINCIPALES
    ### -------------------

    def train(self, dataset, continuous = 0, measureType = MeasureType.GAIN):

        if self.model == ModelOps.DECISION_TREE:
            self.classifier = self.trainTree(dataset, continuous, measureType)

        elif self.model == ModelOps.DECISION_FOREST:
            self.classifier = self.trainForest(dataset, continuous, measureType)

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

    def trainTree(self, dataset, continuous, measureType):

        self.attributes = reader.getAttributes(dataset)
        self.results = reader.getResults(dataset)
        self.dataset = dataset

        return id3Train(self.dataset, self.attributes, self.results, continuous, measureType)

    def classifyTree(self, example):
        return id3Classify(self.classifier, example)

    def trainForest(self, dataset, continuous, measureType):

        self.attributes = reader.getAttributes(dataset)
        self.results = reader.getResults(dataset)
        self.dataset = dataset

        return id3ForestTrain(self.dataset, self.attributes, self.results, continuous, measureType)

    def classifyForest(self, example):
        return id3ForestClassify(self.classifier, example, self.results)

