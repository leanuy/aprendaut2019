### DEPENDENCIAS
### ------------------

import numpy as np
import random

from .decision_tree import id3Train, id3Classify
from .decision_forest import id3ForestTrain, id3ForestClassify
import processing.reader as reader
import processing.parser as parser
from utils.const import ModelOps

### CLASE PRINCIPAL
### ------------------

class Model():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, modelType):
        self.model = modelType
        self.attributes = None
        self.results = None
        self.options = None
        self.classifier = None

    ### GETTERS y SETTERS
    ### -------------------

    def getModelType(self):
        return self.model

    def getDataset(self):
        return self.dataset

    def setDataset(self, dataset):
        self.dataset = dataset
        self.attributes = reader.getAttributes(dataset)
        self.results = reader.getResults(dataset)

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

    def train(self, dataset, attributes, results, options):

        self.attributes = attributes
        self.results = results
        self.options = options

        if self.model == ModelOps.DECISION_TREE:
            self.classifier = self.trainTree(dataset)

        elif self.model == ModelOps.DECISION_FOREST:
            self.classifier = self.trainForest(dataset)

    def classify(self, example, noProb = False):

        if self.model == ModelOps.DECISION_TREE:
            if noProb:
                (classification, p) = self.classifyTree(example)
                return classification
            else:
                return self.classifyTree(example)

        elif self.model == ModelOps.DECISION_FOREST:
            if noProb:
                (classification, p) = self.classifyForest(example)
                return classification
            else:
                return self.classifyForest(example)

    ### METODOS AUXILIARES
    ### -------------------

    def classifySet(self, exampleSet):
        
        resultsSet = exampleSet.copy()

        classification = lambda x : self.classify(x, True)
        resultsSet['class'] = resultsSet.apply(classification, axis=1)
        
        return resultsSet

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

    def trainTree(self, dataset):
        return id3Train(dataset, self.attributes, self.results, self.options)

    def classifyTree(self, example):
        return id3Classify(self.classifier, example)

    def trainForest(self, dataset):
        return id3ForestTrain(dataset, self.attributes, self.results, self.options)

    def classifyForest(self, example):
        return id3ForestClassify(self.classifier, example, self.results)


