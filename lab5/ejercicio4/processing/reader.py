### DEPENDENCIAS
### ------------------
import json
import pandas as pd

from processing.parser import parseCandidates
from utils.const import DATA_CANDIDATOS, DATA_CANDIDATOS_ESPECTRO, DATA_CANDIDATOS_NOLAN, DATA_CANDIDATOS_SIN_PARTIDO, DATA_CANDIDATOS_ESPECTRO_DUAL, CandidateDivision

### METODOS PRINCIPALES
### -------------------

# Lee 'filename' y lo devuelve como un dataframe de pandas optimizado
def readDataset(filename, more_than_1000=True):
    dataset = pd.read_csv(filename)
    candidates = dataset.iloc[:, 1]
    answers = dataset.iloc[:, 2:28]

    # Solo candidatos con mas de mil votos
    if more_than_1000:
        answers['candidateID'] = candidates.copy()
        filtered = answers[answers.candidateID.isin(candidates.value_counts()[candidates.value_counts() > 1000].index.values)]
        answers_toreturn = filtered.iloc[:, :26]
        candidates = filtered.iloc[:, 26]

    general_parties = readParties()
    parties = parseCandidates(candidates, general_parties)
    
    return answers_toreturn.apply(pd.to_numeric, downcast='unsigned'), candidates.apply(pd.to_numeric, downcast='unsigned'), parties.apply(pd.to_numeric, downcast='unsigned')
    
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
            