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

def plotBars(dataset, meta):
    plt.figure(figsize=(12,6)) 
    y_pos = np.arange(len(meta['xlabels']))      
    plt.bar(y_pos, dataset, align='center', alpha=0.8, color=meta['colors'][0])
    plt.xticks(y_pos, meta['xlabels'])
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

def plotPie(dataset, labels, meta):
    plt.figure(figsize=(10,8))
    patches, texts = plt.pie(dataset, colors=meta['colors'], startangle=meta['angle'])
    plt.legend(patches, labels, loc="best")
    plt.title(meta['title'])
    plt.show()

def plotStackedBars(dataset, meta):

    data, classified = dataset

    legend = []
    labels = []
    bottom = np.zeros(meta['lengthClasses'], dtype=int)
    index = 0
    
    # Plotting
    plt.figure(figsize=(16,6))
    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

    for id, name, _, count in data:
        actual = list(classified[id].values())
        barResult = ax.bar(range(meta['lengthClasses']), actual, bottom=bottom, align='center', color=meta['colors'][index])
        
        legend.append(barResult[0])
        labels.append(f"{name} ({round(100*(count/meta['lengthDataset']), 2)}%)")

        # Se guarda la altura para futuras barras.
        bottom += np.array(actual)
        index += 1

    plt.xticks(range(meta['lengthClasses']), meta['classes'])
    plt.legend(list(legend), list(labels), loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title(meta['title'])
    plt.show()

def plotSubBars(dataset_full, meta_full):

    dataset, datasetC = dataset_full
    meta, metaC = meta_full

    plt.figure(figsize=(12,8)) 
  
    plt.subplot(2, 1, 1)
    y_pos = np.arange(len(meta['xlabels']))
    plt.bar(y_pos, dataset, align='center', alpha=0.8, color=meta['colors'][0])
    plt.xticks(y_pos, meta['xlabels'])
    plt.title(meta['title'])

    plt.subplot(2, 1, 2)
    y_pos = np.arange(len(metaC['xlabels']))      
    plt.bar(y_pos, datasetC, align='center', alpha=0.8, color=metaC['colors'][0])
    plt.xticks(y_pos, metaC['xlabels'])      
    plt.title(metaC['title'])

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