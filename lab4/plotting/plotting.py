### DEPENDENCIAS
### ------------------

import numpy as np
import matplotlib.pyplot as plt

### METODOS PRINCIPALES
### ------------------

def plotScatter(dataset, labels, meta):
    # Tamaño fijo para que entren etiquetas
    plt.figure(figsize=(16,6)) 

    # Si no hay etiqueta, es un sólo grupo
    if labels == None:

        # Obtener coordenadas (x,y) del dataset
        x = dataset[:, 0]
        y = dataset[:, 1]

        # Graficar
        plt.scatter(x, y, alpha=0.8, edgecolors='none', s=meta['size'])
    
    # Si hay etiqueta, hay múltiples grupos
    else:
        # Reducir ancho para que entren etiquetas
        ax = plt.subplot(111)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

        index = 0
        for data, label in zip(dataset, labels):

            # Obtener coordenadas (x,y) del dataset
            x = data[:, 0]
            y = data[:, 1]

            # Graficar
            ax.scatter(x, y, alpha=0.8, edgecolors='none', s=meta['size'], color=meta['colors'][index], label=label)
            index += 1

        # Aumentar tamaño de puntos en etiquetas
        lgnd = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        for i in range(0, len(lgnd.legendHandles)):
            lgnd.legendHandles[i]._sizes = [50]
    
    plt.title(meta['title'])
    plt.show()

def plotBars(dataset, labels, meta):

    plt.figure(figsize=(12,6)) 

    y_pos = np.arange(len(labels))      
    plt.bar(y_pos, dataset, align='center', alpha=0.8, color=meta['colors'][0])
    plt.xticks(y_pos, labels)
    
    plt.title(meta['title'])
    plt.show()

def plotCurve(dataset, meta):

    plt.figure(figsize=(12,6)) 

    plt.plot(np.cumsum(dataset), alpha=0.8, color=meta['colors'][0])

    plt.xlabel(meta['xlabel'])
    plt.ylabel(meta['ylabel'])    
    plt.title(meta['title'])
    plt.show()

def plotHeatmap(dataset, meta):

    fig = plt.figure(figsize=(10,8))
    ax = fig.add_subplot(111)
    cax = ax.matshow(dataset, interpolation='nearest')
    fig.colorbar(cax)

    plt.title(meta['title'])
    plt.show()

def plotStackedBars(classes, parties, classified, meta):
    # Variables
    p = {}
    bottom = np.zeros((len(classes),), dtype=int)
    legend = []
    labels = []

    # Plotting
    plt.title(meta['title'])
    for party, partyName, partyCandidates, partyCount in parties:
        actual = list(classified[party].values())
        p[party] = plt.bar(range(len(classes)), actual, bottom=bottom, align='center', color = meta['colors'][party])
        
        legend.append(p[party][0])
        labels.append(f"{partyName} ({round(100*(partyCount/meta['lengthDataset']), 2)}%)")

        # Se guarda la altura para futuras barras.
        bottom += np.array(actual)
    plt.xticks(range(len(classes)), list(classes.keys()))
    plt.legend(list(legend), list(labels), loc=2)
    plt.show()