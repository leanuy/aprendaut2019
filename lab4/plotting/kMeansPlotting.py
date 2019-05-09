### DEPENDENCIAS
### ------------------

import numpy as np
import matplotlib.pyplot as plt

import processing.reader as reader
import processing.parser as parser
import processing.processor as processor
from utils.const import DATA_CANDIDATOS, PCAnalysis
from model.k_means import classify

### METODOS PRINCIPALES
### -------------------

def plotKMeans(classes):
    classified = {}
    colors = 10*["r", "b", "g", "y", "k", "m", "c"]
    for classification, cluster in classes.items():
        classified[classification] = len(cluster)
    
    plt.title("K-Means - Tamaño de clusters")
    plt.bar(range(len(classified)), list(classified.values()), align='center', color = colors)
    plt.xticks(range(len(classified)), list(classified.keys()))
    plt.show()

def plotKMeansParties(dataset, candidates, parsedParties, centroids, classes):
    classified = {}
    partyNames = []
    for party, partyName, partyCandidates in parsedParties:
        partyNames.append(partyName)
        classified[party] = {}
        for classification in classes:
            classified[party][classification] = 0

    for index, row in dataset.iterrows():
        party = processor.getParty(parsedParties, candidates[index])
        classified[party][classify(row.values, centroids)] += 1

    # Variables
    colors = { 0: '#800000', 1: '#e6194B', 2: '#f58231', 3: '#ffe119', 4: '#bfef45', 5: '#3cb44b', 6: '#469990', 7: '#42d4f4', 8: '#000075', 9: '#4363d8', 10: '#911eb4' }
    p = {}
    bottom = np.zeros((len(classes),), dtype=int)
    legend = []

    # Plotting
    plt.title("K-Means - Separado por partidos")
    for party, partyName, partyCandidates in parsedParties:
        actual = list(classified[party].values())
        p[party] = plt.bar(range(len(classes)), actual, bottom=bottom, align='center', color = colors[party])
        legend.append(p[party][0])
        # Se guarda la altura para futuras barras.
        bottom += np.array(actual)
    plt.xticks(range(len(classes)), list(classes.keys()))
    plt.legend(list(legend), list(partyNames), loc=2)
    plt.show()

### METODOS AUXILIARES
### ------------------
