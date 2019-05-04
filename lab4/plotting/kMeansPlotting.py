### DEPENDENCIAS
### ------------------

import numpy as np
import matplotlib.pyplot as plt

import processing.reader as reader
import processing.parser as parser
from utils.const import DATA_CANDIDATOS, PCAnalysis

### METODO PRINCIPAL
### ----------------

def plotKMeans(classes):
    classified = {}
    colors = 10*["r", "b", "g", "y", "k", "m", "c"]
    for classification in classes:
        classified[classification] = len(classes[classification])
    
    plt.title("K-Means Clusters' Length")
    plt.bar(range(len(classified)), list(classified.values()), align='center', color = colors)
    plt.xticks(range(len(classified)), list(classified.keys()))
    plt.show()

def plotKMeansParties(classes, candidates):

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

