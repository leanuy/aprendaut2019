### DEPENDENCIAS
### ------------------

import numpy as np
import random

from .decision_tree import id3Train, id3Classify
from .decision_forest import id3ForestTrain, id3ForestClassify

import processing.reader as reader
import processing.parser as parser

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

    def train(self, dataset, continuous = 0):

        if self.model == ModelOps.DECISION_TREE:
            self.classifier = self.trainTree(dataset, continuous)

        elif self.model == ModelOps.DECISION_FOREST:
            self.classifier = self.trainForest(dataset, continuous)

    def classify(self, example, continuous = 0):

        if self.model == ModelOps.DECISION_TREE:
            return self.classifyTree(example, continuous)

        elif self.model == ModelOps.DECISION_FOREST:
            return self.classifyForest(example, continuous)

    ### METODOS AUXILIARES
    ### -------------------

    def classifySet(self, exampleSet, continuous = 0):
        
        results = []
        
        for example in exampleSet:
            example['class'] = self.classify(example, continuous)
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

    def trainTree(self, dataset, continuous):

        self.attributes = reader.getAttributes(dataset)
        self.results = reader.getResults(dataset)
        self.dataset = dataset
        #self.dataset = parser.getFormattedDataset(dataset, self.attributes, continuous)
        #self.values = reader.getDatasetPossibleValues(self.dataset, self.attributes)

        return id3Train(self.dataset, self.attributes, self.results, continuous)

    def classifyTree(self, example, continuous):
        return id3Classify(self.classifier, example, continuous)

    def trainForest(self, dataset, continuous):

        self.attributes = reader.getAttributes(dataset)
        self.results = reader.getResults(dataset)
        self.dataset = parser.getFormattedDataset(dataset, self.attributes, continuous)
        self.values = reader.getDatasetPossibleValues(self.dataset, self.attributes)

        return id3ForestTrain(self.dataset, self.attributes, self.values, self.results, continuous)

    def classifyForest(self, example, continuous):
        return id3ForestClassify(self.classifier, example, self.results, continuous)

