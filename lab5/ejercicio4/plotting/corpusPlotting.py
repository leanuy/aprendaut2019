### DEPENDENCIAS
### ------------------

from .plotting import plotSubBars

### CONSTANTES
### ------------------

COLORS = ['#f58231', '#4363d8', '#e6194B', '#3cb44b', '#469990', '#ffe119', '#000075', '#bfef45', '#42d4f4', '#9F8BE5', '#9400FF']

### METODO PRINCIPAL
### ----------------

def plotCorpus(dataset_full, datasetC_full, candidatesJSON, partiesJSON):

    dataset, candidates, parties = dataset_full
    datasetC, candidatesC, partiesC = datasetC_full

    # Unir los candidatos a sus respectivos votantes
    dataset['candidateID'] = candidates
    datasetC['candidateID'] = candidatesC

    # Obtener candidatos unicos ordenados por id
    candidates_set = sorted(candidates.unique())
    candidatesC_set = sorted(candidatesC.unique())

    plotCandidates(dataset, datasetC, candidates_set, candidatesC_set, candidatesJSON)

    dataset['partyID'] = parties
    datasetC['partyID'] = partiesC

    parties_set = sorted(parties.unique())
    partiesC_set = sorted(partiesC.unique())
    partiesC_set = [x for x in partiesC_set if x not in parties_set]

    plotParties(dataset, datasetC, parties_set, partiesC_set, partiesJSON)

### METODOS AUXILIARES
### ------------------

def plotCandidates(dataset, datasetC, candidates, candidatesC, candidatesJSON):

    ds = candidates.copy()
    labels = candidates.copy()

    dsC = candidatesC.copy()
    labelsC = candidatesC.copy()

    for candidate in candidatesJSON:

        candidateID = candidate['id']
        candidateName = candidate['name']
        
        if candidateID in candidates:
            index = candidates.index(candidateID)
            labels[index] = f'{candidateID} - {candidateName}'
            ds[index] = len(dataset.loc[dataset['candidateID'] == candidateID].index)

        elif candidateID in candidatesC:
            index = candidatesC.index(candidateID)
            labelsC[index] = f'{candidateID} - {candidateName}'
            dsC[index] = len(datasetC.loc[datasetC['candidateID'] == candidateID].index)

    # Generar metadatos para la gráfica
    meta = {
      'title': 'Candidatos con más de 1000 votos',
      'xlabels': [str(i) for i in candidates],
      'colors': [COLORS[0]]
    }
    metaC = {
      'title': 'Candidatos con menos de 1000 votos',
      'xlabels': [str(i) for i in candidatesC],
      'colors': [COLORS[1]]
    }

    print("Candidatos con más de 1000 votos: ")
    for label in labels:
        print(label)
    print()

    print("Candidatos con menos de 1000 votos: ")
    for label in labelsC:
        print(label)
    print()

    # Generar única gráfica
    plotSubBars((ds, dsC), (meta, metaC))

def plotParties(dataset, datasetC, parties, partiesC, partiesJSON):

    ds = parties.copy()
    labels = parties.copy()

    dsC = partiesC.copy()
    labelsC = partiesC.copy()

    counter = 0
    for party in partiesJSON:

        partyID = counter
        partyName = party['party']
        
        if partyID in parties:
            index = parties.index(partyID)
            labels[index] = f'{partyID} - {partyName}'
            ds[index] = len(dataset.loc[dataset['partyID'] == partyID].index)

        elif partyID in partiesC:
            index = partiesC.index(partyID)
            labelsC[index] = f'{partyID} - {partyName}'
            dsC[index] = len(datasetC.loc[datasetC['partyID'] == partyID].index)

        counter += 1

    # Generar metadatos para la gráfica
    meta = {
      'title': 'Partidos con más de 1000 votos',
      'xlabels': [str(i) for i in parties],
      'colors': [COLORS[0]]
    }
    metaC = {
      'title': 'Partidos con menos de 1000 votos',
      'xlabels': [str(i) for i in partiesC],
      'colors': [COLORS[1]]
    }

    print("Partidos con más de 1000 votos: ")
    for label in labels:
        print(label)
    print()

    print("Partidos con menos de 1000 votos: ")
    for label in labelsC:
        print(label)
    print()

    # Generar única gráfica
    plotSubBars((ds, dsC), (meta, metaC))