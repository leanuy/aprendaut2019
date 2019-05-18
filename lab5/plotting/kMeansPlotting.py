### DEPENDENCIAS
### ------------------

import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

from .plotting import plotPie, plotStackedBars
import processing.reader as reader
import processing.parser as parser
from utils.const import KmeansAnalysis, KmeansEvaluations, CandidateDivision
from model.k_means import classify
from .plotting import plotStackedBars

### CONSTANTES
### ------------------

COLORS = ['#f58231', '#4363d8', '#e6194B', '#3cb44b', '#469990', '#ffe119', '#000075', '#bfef45', '#42d4f4', '#9F8BE5', '#9400FF', '#f68261', '#43D3D8', '#C5694B', '#00BD4b', '#4BBBB0', '#FFEE0F']

### METODO PRINCIPAL
### -------------------

def plotKMeans(dataset, candidates, centroids, classes, options):

    if options['kmeans_analysis'] == KmeansAnalysis.GENERAL:
        plotGenericKMeans(dataset, candidates, centroids, classes)

    if options['kmeans_analysis'] == KmeansAnalysis.CANDIDATES:
        plotCandidatesKMeans(dataset, candidates, centroids, classes, options)

    elif options['kmeans_analysis'] == KmeansAnalysis.PARTIES:
        plotPartiesKMeans(dataset, candidates, centroids, classes, options)

### METODOS AUXILIARES - Analisis
### -----------------------------

def plotGenericKMeans(dataset, candidates, centroids, classes):
    
    # Generar datos para la gráfica
    classified = {}
    labels = []
    for classification, cluster in classes.items():
        classified[classification] = len(cluster)
        labels.append(f'{classification} ({round(len(cluster) * 100 / len(dataset),2)}%)')
    
    # Generar metadatos para la gráfica
    meta = {
      'title': 'K-Means - Distribución por clusters',
      'colors': COLORS,
      'angle': 90
    }

    plotPie(classified.values(), labels, meta)

def plotCandidatesKMeans(dataset, candidates, centroids, classes, options):

    candidatesAux = []
    unique, counts = np.unique(candidates, return_counts=True)
    candidatesCount = dict(zip(unique, counts))

    candidatesJSON = reader.readCandidates(options)   
    candidatesParsed = parser.parseCandidatesFromParties(candidatesJSON, unique)
  
    for candidate, candidateName in candidatesParsed:
        candidatesAux.append((candidate, candidateName, 'dummy', candidatesCount[candidate]))
    candidatesAux = sorted(candidatesAux, key=itemgetter(2), reverse=True)

    # Inicialización estructuras
    classified = {}
    for candidate, candidateName, _, _ in candidatesAux:
        classified[candidate] = {}
        for classification in classes:
            classified[candidate][classification] = 0

    # Re-clasificación del dataset acorde a los centroides y recolección de proporción de cada party en cada cluster.
    for index, row in dataset.iterrows():
        candidate = candidates[index]
        classified[candidate][classify(row.values, centroids)] += 1
    
    # Generar metadatos de la gráfica
    meta = {
      'title': 'K-Means - División por candidato',
      'colors': 2*COLORS,
      'lengthDataset': len(dataset),
      'lengthClasses': len(classes),
      'classes': list(classes.keys())
    }
    plotStackedBars((candidatesAux, classified), meta)

def plotPartiesKMeans(dataset, candidates, centroids, classes, options):

    # Leer archivo JSON de candidatos para parsear candidatos del dataset 
    # Luego, obtener partidos y candidatos parseados
    # - parsedParties: Lista de tuplas (idPartido, nombrePartido, candidatosPartido)
    # - parsedCandidates: Lista de partidos que preserva el orden de candidatos en el dataset original
    partyJSON = reader.readParties(options['candidate_division'], options)    
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
        party = parser.getParty(parties, candidates[index], options['candidate_division'])
        classified[party][classify(row.values, centroids)] += 1
    
    # Generar metadatos de la gráfica
    meta = {
      'title': 'K-Means - División por partido político',
      'colors': COLORS,
      'lengthDataset': len(dataset),
      'lengthClasses': len(classes),
      'classes': list(classes.keys())
    }
    plotStackedBars((parties, classified), meta)
