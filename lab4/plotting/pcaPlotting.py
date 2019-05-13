### DEPENDENCIAS
### ------------------

import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

from .plotting import plotScatter, plotHeatmap, plotBars, plotCurve
import processing.reader as reader
import processing.parser as parser
from utils.const import PCAnalysis, PCAIntermediates, CandidateDivision

### CONSTANTES
### ------------------

COLORS = ['#f58231', '#4363d8', '#e6194B', '#3cb44b', '#469990', '#ffe119', '#000075', '#bfef45', '#42d4f4', '#9F8BE5', '#9400FF']

### METODO PRINCIPAL
### ----------------

def plotPCA(dataset, candidates, options, extras):

    if options['pca_analysis'] == PCAnalysis.GENERAL:
        plotGenericPCA(dataset)

    elif options['pca_analysis'] == PCAnalysis.ALL_PARTY:
        plotAllPartyPCA(dataset, candidates, options)

    elif options['pca_analysis'] == PCAnalysis.EACH_PARTY:
        plotEachPartyPCA(dataset, candidates, options)

    if options['pca_intermediates'] == PCAIntermediates.COV_MATRIX:
        plotCovMatrix(extras['cov_matrix'])

    elif options['pca_intermediates'] == PCAIntermediates.EIGEN_VALUES:
        plotEigenValues(extras['eigen_values'])

    elif options['pca_intermediates'] == PCAIntermediates.VARIANCE_RATIO:
        plotVarianceRatio(extras['explained_variance_ratio'])
        
### METODOS AUXILIARES - Analisis
### -----------------------------

def plotGenericPCA(dataset):
    # Generar metadatos de la gráficar
    meta = {
      'title': 'Corpus en 2 dimensiones (PCA)',
      'size': 4
    }

    # Generar gráfica general de puntos
    plotScatter(dataset, None, meta)

def plotAllPartyPCA(dataset, candidates, options):
    # Leer archivo JSON de candidatos para parsear candidatos del dataset 
    # Luego, obtener partidos y candidatos parseados
    # - parsedParties: Lista de tuplas (idPartido, nombrePartido, candidatosPartido)
    # - parsedCandidates: Lista de partidos que preserva el orden de candidatos en el dataset original
    partyJSON = reader.readParties(options['candidate_division'], options)    
    parsedParties, parsedCandidates = parser.parseCandidates(candidates.values, partyJSON)

    # Agregar partidos al dataset
    results = np.column_stack((dataset, parsedCandidates.transpose()))

    # Procesar y generar estructura para guardar los resultados por partido junto a su nombre
    aux = []
    for party, partyName, partyCandidates in parsedParties:

        # Generar subconjunto de dataset para un partido
        partyResults = results[results[:,2] == party]
        partyResults = partyResults[:,[0,1]]

        # Generar etiqueta con nombre de partido y porcentaje de votos
        prob = (len(partyResults) / (len(results))) * 100
        partyName += ' (' + str(round(prob, 2)) + '%)'

        aux.append((prob, partyName, partyResults))

    # Ordenar datos por porcentaje de votos y separar en dos listas
    aux = sorted(aux, key=itemgetter(0), reverse=True)
    data = []
    labels = []
    for prob, partyName, partyResults in aux:
        data.append(partyResults)
        labels.append(partyName)

    # Generar metadatos de la gráfica
    meta = {
      'title': 'Corpus en 2 dimensiones (PCA) - División por partido político',
      'size': 8,
      'colors': COLORS
    }

    # Generar gráfica general de puntos
    plotScatter(data, labels, meta)

def plotEachPartyPCA(dataset, candidates, options):

    # Leer archivo JSON de candidatos para parsear candidatos del dataset 
    # Luego, obtener partidos y candidatos parseados
    # - parsedParties: Lista de tuplas (idPartido, nombrePartido, candidatosPartido)
    # - parsedCandidates: Lista de partidos que preserva el orden de candidatos en el dataset original
    partyJSON = reader.readParties(CandidateDivision.PARTIES, options)   
    parsedParties, parsedCandidates = parser.parseCandidates(candidates.values, partyJSON)

    # Agregar partidos al dataset
    results = np.column_stack((dataset, parsedCandidates.transpose()))

    # Procesar y generar estructura para guardar los resultados por partido junto a su nombre
    aux = []
    for party, partyName, partyCandidates in parsedParties:

        # Generar subconjunto de dataset para un partido
        partyResults = results[results[:,2] == party]
        partyResults = partyResults[:,[0,1]]

        # Generar etiqueta con nombre de partido y porcentaje de votos
        prob = (len(partyResults) / (len(results))) * 100
        partyName += ' (' + str(round(prob, 2)) + '%)'

        aux.append((prob, partyName, partyResults))

    # Ordenar datos por porcentaje de votos y separar en dos listas
    aux = sorted(aux, key=itemgetter(0), reverse=True)
    data = []
    labels = []
    probs = []
    for prob, partyName, partyResults in aux:
        data.append(partyResults)
        labels.append(partyName)
        probs.append(prob)

    # Generar metadatos de la gráfica
    meta = {
      'title': 'Corpus en 2 dimensiones (PCA) - División para cada partido político',
      'size': 4,
      'colors': [COLORS[0], COLORS[1]]
    }

    # Graficar para cada partido
    for i in range(0, len(data)):
    
        # Agrupar todos los partidos menos el i-ésimo
        otherParties = list(data)
        otherParties.pop(i)              
        otherParties = np.concatenate( otherParties, axis=0 )

        # Generar estructuras auxiliares
        auxData = [data[i], otherParties]
        auxLabels = [labels[i], 'Otros (' + str(round(100 - probs[i], 2)) + '%)']

        # Generar gráfica general de puntos
        plotScatter(auxData, auxLabels, meta)

### METODOS AUXILIARES - Resultados intermedios
### -------------------------------------------

def plotCovMatrix(cov_matrix):

    # Generar metadatos para la gráfica
    meta = {
      'title': 'Matriz de Covarianza del Corpus - Relación entre atributos'
    }

    # Generar única gráfica
    plotHeatmap(cov_matrix, meta)

def plotEigenValues(eigen_values):

    # Generar metadatos para la gráfica
    meta = {
      'title': 'Matriz de Covarianza del Corpus - Distribución de valores propios',
      'xlabels': [str(i) for i in range(0, len(eigen_values))],
      'colors': [COLORS[0]]
    }

    # Generar única gráfica
    plotBars(eigen_values, meta)
    
def plotVarianceRatio(variance_ratio):

    # Generar metadatos para la gráfica
    meta = {
      'title': 'Ratio de Varianza',
      'xlabel': 'Número de Componentes',
      'ylabel': '% Varianza',
      'colors': [COLORS[0]]
    }

    # Generar única gráfica
    plotCurve(variance_ratio, meta)