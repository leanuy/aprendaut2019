### DEPENDENCIAS
### ------------------

import numpy as np
import matplotlib.pyplot as plt

import processing.reader as reader
import processing.parser as parser
from utils.const import DATA_CANDIDATOS, PCAnalysis, PCAIntermediates

### METODO PRINCIPAL
### ----------------

def plotPCA(dataset, candidates, options, extras):

    if options['pca_analysis'] == PCAnalysis.GENERAL:
        plotGenericPCA(dataset)

    elif options['pca_analysis'] == PCAnalysis.ALL_PARTY:
        plotAllPartyPCA(dataset, candidates)

    elif options['pca_analysis'] == PCAnalysis.EACH_PARTY:
        plotEachPartyPCA(dataset, candidates)

    if options['pca_intermediates'] == PCAIntermediates.COV_MATRIX:
        plotCovMatrix(extras['cov_matrix'])

    elif options['pca_intermediates'] == PCAIntermediates.EIGEN_VALUES:
        plotEigenValues(extras['eigen_values'])
    

### METODOS AUXILIARES - Analisis
### -----------------------------

def plotGenericPCA(dataset):
    x_number_list = dataset[:, 0]
    y_number_list = dataset[:, 1]

    plt.scatter(x_number_list, y_number_list, s=1)
    plt.title("PCA a 2 Dimensiones")
    plt.show()

def plotAllPartyPCA(dataset, candidates):

    partyJSON = reader.readParties(DATA_CANDIDATOS)
    parsedParties, parsedCandidates = parser.parseCandidates(candidates.values, partyJSON)
    
    results = np.column_stack((dataset, parsedCandidates.transpose()))

    data = []
    for party, partyName, partyCandidates in parsedParties:
        partyResults = results[results[:,2] == party]
        partyResults = partyResults[:,[0,1]]
        data.append((partyName, partyResults))

    for partyName, partyResults in data:
        x = partyResults[:, 0]
        y = partyResults[:, 1]

        prob = (len(partyResults) / (len(results))) * 100
        partyName += ' (' + str(round(prob, 2)) + '%)'

        plt.scatter(x, y, alpha=0.8, edgecolors='none', s=5, label=partyName)

    plt.title('PCA - Separado por partidos')
    plt.legend(loc=2)
    plt.show()

def plotEachPartyPCA(dataset, candidates):
    
    partyJSON = reader.readParties(DATA_CANDIDATOS)
    parsedParties, parsedCandidates = parser.parseCandidates(candidates.values, partyJSON)
    
    results = np.column_stack((dataset, parsedCandidates.transpose()))

    data = []
    for party, partyName, partyCandidates in parsedParties:
        partyResults = results[results[:,2] == party]
        partyResults = partyResults[:,[0,1]]
        data.append(partyResults)

    for i in range(0, len(data)):

        party, partyName, partyCandidates = parsedParties[i]
    
        oneParty = data[i]
        xOneParty = oneParty[:, 0]
        yOneParty = oneParty[:, 1]
      
        otherParties = list(data)
        otherParties.pop(i)              
        otherParties = np.concatenate( otherParties, axis=0 )
        xOtherParties = otherParties[:, 0]
        yOtherParties = otherParties[:, 1]

        prob = (len(oneParty) / (len(otherParties) + len(oneParty))) * 100
        partyName += ' (' + str(round(prob, 2)) + '%)'

        plt.scatter(xOneParty, yOneParty, alpha=0.8, edgecolors='none', s=5, label=partyName)        
        plt.scatter(xOtherParties, yOtherParties, alpha=0.8, edgecolors='none', s=5, label='Otros (' + str(round(100 - prob, 2)) + '%)')

        plt.title('PCA - Separado para partido: ' + str(partyName))
        plt.legend(loc=2)
        plt.show()

### METODOS AUXILIARES - Resultados intermedios
### -------------------------------------------

def plotCovMatrix(cov_matrix):

    rows, columns = cov_matrix.shape

    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(cov_matrix, interpolation='nearest')
    fig.colorbar(cax)

    plt.show()

def plotEigenValues(eigen_values):
    labels = [str(i) for i in range(0, len(eigen_values))]
    y_pos = np.arange(len(labels))

    plt.bar(y_pos, eigen_values, align='center', alpha=0.5)
    plt.xticks(y_pos, labels)
    plt.ylabel('Valores propios')
    plt.title('Distribución de valores propios')

    plt.show()