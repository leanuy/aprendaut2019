### DEPENDENCIAS
### ------------------

import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

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

    parties = []
    unique, counts = np.unique(parsedCandidates, return_counts=True)
    partiesCount = dict(zip(unique, counts))
    for party, partyName, partyCandidates in parsedParties:
        parties.append((party, partyName, partyCandidates, partiesCount[party]))
    
    parties = sorted(parties, key=itemgetter(3), reverse=True)

    classified = {}
    partyNames = []
    for party, partyName, partyCandidates, partyCount in parties:
        partyNames.append(partyName)
        classified[party] = {}
        for classification in classes:
            classified[party][classification] = 0

    for index, row in dataset.iterrows():
        party = parser.getParty(parties, candidates[index], division)
        classified[party][classify(row.values, centroids)] += 1
    
    # Generar metadatos de la gráfica
    meta = {
      'title': 'K-Means - División por partido político',
      'colors': ['#f58231', '#4363d8', '#e6194B', '#3cb44b', '#469990', '#ffe119', '#000075', '#bfef45', '#42d4f4', '#9F8BE5', '#9400FF']
    }

    # Variables
    p = {}
    bottom = np.zeros((len(classes),), dtype=int)
    legend = []

    # Plotting
    plt.title(meta['title'])
    for party, partyName, partyCandidates, partyCount in parties:
        actual = list(classified[party].values())
        p[party] = plt.bar(range(len(classes)), actual, bottom=bottom, align='center', color = meta['colors'][party])
        legend.append(p[party][0])
        # Se guarda la altura para futuras barras.
        bottom += np.array(actual)
    plt.xticks(range(len(classes)), list(classes.keys()))
    plt.legend(list(legend), list(partyNames), loc=2)
    plt.show()

### METODOS AUXILIARES - Resultados
### -----------------------------
