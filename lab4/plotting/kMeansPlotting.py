### DEPENDENCIAS
### ------------------

import numpy as np
import matplotlib.pyplot as plt

import processing.reader as reader
import processing.parser as parser
from utils.const import DATA_CANDIDATOS, DATA_CANDIDATOS_ESPECTRO, DATA_CANDIDATOS_NOLAN, KmeansAnalysis, KmeansEvaluations, CandidateDivision
from model.k_means import classify

### METODO PRINCIPAL
### -------------------

def plotKMeans(dataset, candidates, centroids, classes, options, extras):

    if options['kmeans_analysis'] == KmeansAnalysis.GENERAL:
        plotGenericKMeans(classes)

    elif options['kmeans_analysis'] == KmeansAnalysis.PARTIES:
        plotPartiesKMeans(dataset, candidates, centroids, classes, options['candidate_division'])


### METODOS AUXILIARES - Analisis
### -----------------------------

def plotGenericKMeans(classes):
    classified = {}
    colors = 10*["r", "b", "g", "y", "k", "m", "c"]
    for classification, cluster in classes.items():
        classified[classification] = len(cluster)
    
    plt.title("K-Means - Tamaño de clusters")
    plt.bar(range(len(classified)), list(classified.values()), align='center', color = colors)
    plt.xticks(range(len(classified)), list(classified.keys()))
    plt.show()

def plotPartiesKMeans(dataset, candidates, centroids, classes, division):

    # Leer archivo JSON de candidatos para parsear candidatos del dataset 
    partyJSON = None
    if division == CandidateDivision.PARTIES:
        partyJSON = reader.readParties(DATA_CANDIDATOS)
    elif division == CandidateDivision.SPECTRUM:
        partyJSON = reader.readParties(DATA_CANDIDATOS_ESPECTRO)
    elif division == CandidateDivision.NOLAN:
        partyJSON = reader.readParties(DATA_CANDIDATOS_NOLAN)

    # Obtener partidos y candidatos parseados
    # - parsedParties: Lista de tuplas (idPartido, nombrePartido, candidatosPartido)
    # - parsedCandidates: Lista de partidos que preserva el orden de candidatos en el dataset original
    parsedParties, parsedCandidates = parser.parseCandidates(candidates.values, partyJSON)

    classified = {}
    partyNames = []
    for party, partyName, partyCandidates in parsedParties:
        partyNames.append(partyName)
        classified[party] = {}
        for classification in classes:
            classified[party][classification] = 0

    for index, row in dataset.iterrows():
        party = parser.getParty(parsedParties, candidates[index])
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

### METODOS AUXILIARES - Resultados
### -----------------------------
