### DEPENDENCIAS
### ------------------

import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

import processing.reader as reader
import processing.parser as parser
from utils.const import DATA_CANDIDATOS, DATA_CANDIDATOS_ESPECTRO, DATA_CANDIDATOS_NOLAN, KmeansAnalysis, KmeansEvaluations, CandidateDivision
from model.k_means import classify
from .plotting import plotStackedBars

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
    partyJSON = getJSON(division)

    # Obtener partidos y candidatos parseados
    # - parsedParties: Lista de tuplas (idPartido, nombrePartido, candidatosPartido)
    # - parsedCandidates: Lista de partidos que preserva el orden de candidatos en el dataset original
    parsedParties, parsedCandidates = parser.parseCandidates(candidates.values, partyJSON)

    # Ordenamiento de parsedParties según la proporción de votos de cada una.
    parties = []
    unique, counts = np.unique(parsedCandidates, return_counts=True)
    partiesCount = dict(zip(unique, counts))
    for party, partyName, partyCandidates in parsedParties:
        parties.append((party, partyName, partyCandidates, partiesCount[party]))
    parties = sorted(parties, key=itemgetter(3), reverse=True)

    # Inicialización estructuras
    classified = {}
    for party, partyName, partyCandidates, partyCount in parties:
        classified[party] = {}
        for classification in classes:
            classified[party][classification] = 0

    # Re-clasificación del dataset acorde a los centroides y recolección de proporción de cada party en cada cluster.
    for index, row in dataset.iterrows():
        party = parser.getParty(parties, candidates[index], division)
        classified[party][classify(row.values, centroids)] += 1
    
    # Generar metadatos de la gráfica
    # TODO: Esto puede ser movido para una función auxiliar o inclusive cambiar getJSON por getData (que devuelva (json, meta)) y de los colores correctos para cada división (En el orden del json)
    meta = {
      'title': 'K-Means - División por partido político',
      'colors': ['#f58231', '#4363d8', '#e6194B', '#3cb44b', '#469990', '#ffe119', '#000075', '#bfef45', '#42d4f4', '#9F8BE5', '#9400FF'],
      'lengthDataset': len(dataset)
    }
    plotStackedBars(classes, parties, classified, meta)

### METODOS AUXILIARES - Resultados
### -----------------------------

def getJSON(division):
    if division == CandidateDivision.PARTIES:
        return reader.readParties(DATA_CANDIDATOS)
    elif division == CandidateDivision.SPECTRUM:
        return reader.readParties(DATA_CANDIDATOS_ESPECTRO)
    elif division == CandidateDivision.NOLAN:
        return reader.readParties(DATA_CANDIDATOS_NOLAN)