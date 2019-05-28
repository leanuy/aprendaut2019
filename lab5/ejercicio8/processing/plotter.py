### DEPENDENCIAS
### ------------------

import numpy as np
import matplotlib.pyplot as plt

from utils.const import PlayerType, CompareOps, InputLayerTypes, ActivationFunctions, LearningRateOps

### CONSTANTES
### ------------------

COLORS = ['#f58231', '#4363d8', '#e6194B', '#3cb44b', '#469990', '#ffe119', '#000075', '#bfef45', '#42d4f4', '#9F8BE5', '#9400FF']

### METODOS PRINCIPALES
### ------------------

# Grafica resultado de cada partida de un entrenamiento
def printResultsPlot(axis, iterations, filename = None):
    (x_axis, y_axis) = axis
    plt.plot(x_axis, y_axis, 'ro')
    plt.axis([0, iterations - 1, -2, 2])
    if filename == None:
        plt.show()
    else:
        plt.savefig('results/' + filename + '.png')

# Grafica error cuadrático medio de los ajustes de un entrenamiento
def printErrorPlot(plots, iterations):
    sublist = generateErrorSublist(iterations)
    sublistPlots = [x for x in plots if plots.index(x) in sublist]
    fig, ax = plt.subplots()
    for pairs in sublistPlots:
        (x_axis, y_axis) = pairs
        ax.plot(x_axis, y_axis, label="Iter " + str(sublistPlots.index(pairs)))
    ax.legend()

    plt.show()

# Grafica el ratio de partidas ganadas o victorias para todos los modelos entrenados VS cierto tipo de jugador
def plotWinRate(metricType, playerType, winRateMetrics, winRateBoard):

    if metricType == CompareOps.WIN_RATE:

        color_metrics = COLORS[0]
        color_board = COLORS[1]

        if playerType == PlayerType.TRAINED_RANDOM:
            title_metrics = 'Ratio de partidas ganadas - VS Random, Representación con métricas'
            title_board = 'Ratio de partidas ganadas - VS Random, Representación con celdas'

        elif playerType == PlayerType.TRAINED_SELF:
            title_metrics = 'Ratio de partidas ganadas - VS Si Mismo, Representación con métricas'
            title_board = 'Ratio de partidas ganadas - VS Si Mismo, Representación con celdas'

    elif metricType == CompareOps.VICTORY_RATE:

        color_metrics = COLORS[2]
        color_board = COLORS[4]

        if playerType == PlayerType.TRAINED_RANDOM:
            title_metrics = 'Ratio de victorias - VS Random, Representación con métricas'
            title_board = 'Ratio de victorias - VS Random, Representación con celdas'

        elif playerType == PlayerType.TRAINED_SELF:
            title_metrics = 'Ratio de victorias - VS Si Mismo, Representación con métricas'
            title_board = 'Ratio de victorias - VS Si Mismo, Representación con celdas'

    meta_metrics = {
      'title': title_metrics,
      'xlabels': [str(i+1) for i in range(0, len(winRateMetrics))],
      'colors': [color_metrics]
    }

    meta_board = {
      'title': title_board,
      'xlabels': [str(i+1) for i in range(0, len(winRateBoard))],      
      'colors': [color_board]
    }

    plotSubBars((winRateMetrics, winRateBoard), (meta_metrics, meta_board))

# Grafica el promedio del ratio de partidas ganadas para todos los modelos según sus capas ocultas
def plotHiddenLayersWinRate(hiddenLayersData, hiddenNeuronsData):

    labels = ['VS Random, Métricas', 'VS Random, Celdas', 'VS Si Mismo, Metricas', 'VS Si Mismo, Celdas']
    labelsC = ['VS Random, Métricas', 'VS Random, Celdas', 'VS Si Mismo, Metricas', 'VS Si Mismo, Celdas']

    meta_layers = {
      'title': 'Ratio de partidas ganadas - Capas Ocultas',
      'xlabel': 'Número de capas ocultas',
      'ylabel': 'Ratio de partidas ganadas',
      'xticks': ('1', '2', '3'),
      'colors': [COLORS[0], COLORS[1], COLORS[2], COLORS[4]]
    }

    meta_neurons = {
      'title': 'Ratio de partidas ganadas - Neuronas Ocultas',
      'xlabel': 'Número de neuronas por capa oculta',
      'ylabel': 'Ratio de partidas ganadas',
      'xticks': ('1', '100'),      
      'colors': [COLORS[0], COLORS[1], COLORS[2], COLORS[4]]
    }

    plotSubCurves((hiddenLayersData, hiddenNeuronsData), (labels, labelsC), (meta_layers, meta_neurons))

# Grafica el promedio del ratio de partidas ganadas para todos los modelos según su función de activación
def plotActivationWinRate(data):

    labels = ['VS Random, Métricas', 'VS Random, Celdas', 'VS Si Mismo, Metricas', 'VS Si Mismo, Celdas']

    meta = {
      'title': 'Ratio de partidas ganadas - Función de activación',
      'xlabel': 'Tipo de función de activación',
      'ylabel': 'Ratio de partidas ganadas',
      'xticks': ('Sigmoide', 'ReLU', 'TanH'),
      'colors': [COLORS[0], COLORS[1], COLORS[2], COLORS[4]]
    }

    plotCurve(data, labels, meta)

# Grafica el promedio del ratio de partidas ganadas para todos los modelos según su ratio de aprendizaje
def plotLearningRateWinRate(data):

    labels = ['VS Random, Métricas', 'VS Random, Celdas', 'VS Si Mismo, Metricas', 'VS Si Mismo, Celdas']

    meta = {
      'title': 'Ratio de partidas ganadas - Ratio de Aprendizaje',
      'xlabel': 'Tipo de ratio de aprendizaje',
      'ylabel': 'Ratio de partidas ganadas',
      'xticks': ('Constante - 0.0001', 'Variable - 0.1'),
      'colors': [COLORS[0], COLORS[1], COLORS[2], COLORS[4]]
    }

    plotCurve(data, labels, meta)

### METODOS AUXILIARES - GRAFICAS
### -----------------------------

def plotBars(dataset, meta):
    plt.figure(figsize=(12,6)) 
    y_pos = np.arange(len(meta['xlabels']))      
    plt.bar(y_pos, dataset, align='center', alpha=0.8, color=meta['colors'][0])
    plt.xticks(y_pos, meta['xlabels'])
    plt.title(meta['title'])
    plt.show()

def plotCurve(dataset, labels, meta):
    plt.figure(figsize=(12 ,6))
    index = 0
    for d in dataset:
        plt.plot(d, alpha=0.8, color=meta['colors'][index], label=labels[index])
        index += 1
    plt.xticks(np.arange(len(meta['xticks'])), meta['xticks'])
    plt.xlabel(meta['xlabel'])
    plt.ylabel(meta['ylabel'])   
    plt.title(meta['title'])
    plt.legend(labels, loc='upper left')
    plt.grid()
    plt.show()

def plotSubBars(dataset_full, meta_full):

    dataset, datasetC = dataset_full
    meta, metaC = meta_full

    plt.figure(figsize=(16,8)) 
  
    plt.subplot(2, 1, 1)
    y_pos = np.arange(len(meta['xlabels']))
    plt.bar(y_pos, dataset, align='center', alpha=0.8, color=meta['colors'][0])
    plt.xticks(y_pos, meta['xlabels'])
    plt.title(meta['title'])
    plt.ylim([0, 1])

    plt.subplot(2, 1, 2)
    y_pos = np.arange(len(metaC['xlabels']))      
    plt.bar(y_pos, datasetC, align='center', alpha=0.8, color=metaC['colors'][0])
    plt.xticks(y_pos, metaC['xlabels'])      
    plt.title(metaC['title'])
    plt.ylim([0, 1])

    plt.show()

def plotSubCurves(dataset_full, labels_full, meta_full):

    dataset, datasetC = dataset_full
    labels, labelsC = labels_full    
    meta, metaC = meta_full

    plt.figure(figsize=(16,12)) 
  
    plt.subplot(2, 1, 1)
    index = 0
    for d in dataset:
        plt.plot(d, alpha=0.8, color=meta['colors'][index], label=labels[index])
        index += 1
    plt.xticks(np.arange(len(meta['xticks'])), meta['xticks'])
    plt.xlabel(meta['xlabel'])
    plt.ylabel(meta['ylabel'])   
    plt.title(meta['title'])
    plt.legend(labels, loc='upper left')
    plt.grid()

    plt.subplot(2, 1, 2)
    index = 0
    for d in datasetC:
        plt.plot(d, alpha=0.8, color=metaC['colors'][index], label=labelsC[index])
        index += 1
    plt.xticks(np.arange(len(metaC['xticks'])), metaC['xticks'])
    plt.xlabel(metaC['xlabel'])
    plt.ylabel(metaC['ylabel'])    
    plt.title(metaC['title'])
    plt.legend(labelsC, loc='upper left')
    plt.grid()

    plt.show()

def plotGroupBars(dataset, labels, meta):

    pos = [0, len(dataset)]
    width = 0.8
      
    # Plotting the bars
    fig, ax = plt.subplots(figsize=(12,6))

    for i in range(0, len(dataset)):

        plt.bar([p + width*i for p in pos], 
                dataset[i], 
                width,
                alpha=0.8,
                color=meta['colors'][i],
                label=labels[i]) 

    ax.set_xticks([p + (len(dataset)/2) * width for p in pos])
    ax.set_xticklabels(meta['xlabels'])

    plt.ylim([0, 1])
    ax.set_title(meta['title'])
    plt.legend(labels, loc='upper left')
    plt.show()

### METODOS AUXILIARES - PROCESAMIENTO
### ----------------------------------

def generateErrorSublist(iterations):
    if iterations <= 10:
        return list(range(0, iterations))
    elif iterations <= 100:
        return list(range(0, iterations, 10))
    else:
        return list(range(0, iterations, 100))