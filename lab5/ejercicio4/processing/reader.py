### DEPENDENCIAS
### ------------------
import json
import pandas as pd

from processing.parser import parseCandidates
from utils.const import DATA_CANDIDATOS, DATA_CANDIDATOS_ESPECTRO, DATA_CANDIDATOS_NOLAN, DATA_CANDIDATOS_SIN_PARTIDO, DATA_CANDIDATOS_ESPECTRO_DUAL, CandidateDivision

### METODOS PRINCIPALES
### -------------------

# Lee 'filename' y lo devuelve como un dataframe de pandas optimizado
def readDatasetCandidatosMasMil(filename, options = {'from_notebook': False}):
    dataset = pd.read_csv(filename)
    candidates = dataset.iloc[:, 1]
    answers = dataset.iloc[:, 2:28]

    # Solo candidatos con mas de mil votos
    answers['candidateID'] = candidates.copy()
    filtered = answers[answers.candidateID.isin(candidates.value_counts()[candidates.value_counts() > 1000].index.values)]
    answers = filtered.iloc[:, :26]
    candidates = filtered.iloc[:, 26]

    general_parties = readParties(options)
    parties = parseCandidates(candidates, general_parties)
    
    return answers.apply(pd.to_numeric, downcast='unsigned'), candidates.apply(pd.to_numeric, downcast='unsigned'), parties.apply(pd.to_numeric, downcast='unsigned')

def readDatasetCandidatosMenosMil(filename, options = {'from_notebook': False}):
    dataset = pd.read_csv(filename)
    candidates = dataset.iloc[:, 1]
    answers = dataset.iloc[:, 2:28]

    answers['candidateID'] = candidates
    filtered = answers[answers.candidateID.isin(candidates.value_counts()[candidates.value_counts() < 1000].index.values)]
    answers = filtered.iloc[:, :26]
    candidates = filtered.iloc[:, 26]

    general_parties = readParties(options)
    parties = parseCandidates(candidates, general_parties)
        
    return answers.apply(pd.to_numeric, downcast='unsigned'), candidates.apply(pd.to_numeric, downcast='unsigned'), parties.apply(pd.to_numeric, downcast='unsigned')
    
def readDatasetPartiesMasMil(filename, options = {'from_notebook': False}):
    dataset = pd.read_csv(filename)
    candidates = dataset.iloc[:, 1]
    answers = dataset.iloc[:, 2:28]

    general_parties = readParties(options)
    parties = parseCandidates(candidates, general_parties)

    answers['parties'] = parties
    answers['candidateID'] = candidates
    filtered = answers[answers.parties.isin(parties.value_counts()[parties.value_counts() > 1000].index.values)]
    answers = filtered.iloc[:, :26]
    parties = filtered.iloc[:, 26]
    candidates = filtered.iloc[:, 27]

    return answers.apply(pd.to_numeric, downcast='unsigned'), candidates.apply(pd.to_numeric, downcast='unsigned'), parties.apply(pd.to_numeric, downcast='unsigned')

def readDatasetPartiesMenosMil(filename, options = {'from_notebook': False}):
    dataset = pd.read_csv(filename)
    candidates = dataset.iloc[:, 1]
    answers = dataset.iloc[:, 2:28]

    general_parties = readParties(options)
    parties = parseCandidates(candidates, general_parties)

    answers['parties'] = parties
    answers['candidateID'] = candidates
    filtered = answers[answers.parties.isin(parties.value_counts()[parties.value_counts() < 1000].index.values)]
    answers = filtered.iloc[:, :26]
    parties = filtered.iloc[:, 26]
    candidates = filtered.iloc[:, 27]

    return answers.apply(pd.to_numeric, downcast='unsigned'), candidates.apply(pd.to_numeric, downcast='unsigned'), parties.apply(pd.to_numeric, downcast='unsigned')


# Lee partidos de DATA_CANDIDATOS y lo devuelve como archivo JSON
def readParties(options = {'from_notebook': False}):
    if options['from_notebook']:
        filename = '../' + DATA_CANDIDATOS
    else:
        filename = DATA_CANDIDATOS

    with open(filename) as json_file:  
        data = json.load(json_file)
    return data

# Lee partidos de DATA_CANDIDATOS_SIN_PARTIDO y lo devuelve como archivo JSON
def readCandidates(options = {'from_notebook': False}):
    if options['from_notebook']:
        filename = '../' + DATA_CANDIDATOS_SIN_PARTIDO
    else:
        filename = DATA_CANDIDATOS_SIN_PARTIDO

    with open(filename) as json_file:  
        data = json.load(json_file)
    return data
            