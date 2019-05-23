### DEPENDENCIAS
### ------------------
import json
import pandas as pd

from processing.parser import candidates_party
from utils.const import DATA_CANDIDATOS, DATA_CANDIDATOS_ESPECTRO, DATA_CANDIDATOS_NOLAN, DATA_CANDIDATOS_SIN_PARTIDO, DATA_CANDIDATOS_ESPECTRO_DUAL, CandidateDivision

### METODOS PRINCIPALES
### -------------------

# Lee 'filename' y lo devuelve como un dataframe de pandas optimizado
def readDataset(filename, more_than_1000=True):
    dataset = pd.read_csv(filename)
    candidates = dataset.iloc[1:, 1]
    answers = dataset.iloc[1:, 2:28]

    # 
    parties_json = readParties({'from_notebook': False})
    candidates_party_data = {}
    party_index = 0

    for party in parties_json:
        for candidate in party['candidates']:
            candidates_party_data[candidate['id']] = party_index
        party_index += 1

    parties = candidates.apply(lambda x: candidates_party(x, candidates_party_data))

    # Solo candidatos con mas de mil votos
    if more_than_1000:
        answers['candidateID'] = candidates
        answers['partyID'] = parties
        filtered = answers[answers.candidateID.isin(candidates.value_counts()[candidates.value_counts() > 1000].index.values)]
        candidates = filtered['candidateID']
        # answers = filtered.iloc[1:, 2:28]
        parties = filtered['partyID']
        filtered.pop('candidateID')
        filtered.pop('partyID')
        answers = filtered
        
    return answers.apply(pd.to_numeric, downcast='unsigned'), candidates.apply(pd.to_numeric, downcast='unsigned'), parties.apply(pd.to_numeric, downcast='unsigned')
    
# Lee partidos de DATA_CANDIDATOS y lo devuelve como archivo JSON
def readParties(options):
    if options['from_notebook']:
        filename = '../' + DATA_CANDIDATOS
    else:
        filename = DATA_CANDIDATOS

    with open(filename) as json_file:  
        data = json.load(json_file)
    return data

# Lee partidos de DATA_CANDIDATOS_SIN_PARTIDO y lo devuelve como archivo JSON
def readCandidates(options):
    if options['from_notebook']:
        filename = '../' + DATA_CANDIDATOS_SIN_PARTIDO
    else:
        filename = DATA_CANDIDATOS_SIN_PARTIDO

    with open(filename) as json_file:  
        data = json.load(json_file)
    return data
            