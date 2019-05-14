### DEPENDENCIAS
### ------------------
import json
import pandas as pd

from utils.const import DATA_CANDIDATOS, DATA_CANDIDATOS_ESPECTRO, DATA_CANDIDATOS_NOLAN, DATA_CANDIDATOS_SIN_PARTIDO, DATA_CANDIDATOS_ESPECTRO_DUAL, CandidateDivision

### METODOS PRINCIPALES
### -------------------

# Lee 'filename' y lo devuelve como un dataframe de pandas optimizado
def readDataset(filename, is_for_pca=True):
    dataset = pd.read_csv(filename)
    candidates = dataset.iloc[1:, 1]
    answers = dataset.iloc[1:, 2:28]
    return candidates.apply(pd.to_numeric, downcast='unsigned'), answers.apply(pd.to_numeric, downcast='unsigned')

# Lee 'filename' y lo devuelve como archivo JSON
def readParties(division, options):

    if options['from_notebook']:
        filename = '../'
    else:
        filename = ''

    if division == CandidateDivision.PARTIES:
        filename += DATA_CANDIDATOS
    elif division == CandidateDivision.SPECTRUM:
        filename += DATA_CANDIDATOS_ESPECTRO
    elif division == CandidateDivision.DUAL_SPECTRUM:
        filename += DATA_CANDIDATOS_ESPECTRO_DUAL
    elif division == CandidateDivision.NOLAN:
        filename += DATA_CANDIDATOS_NOLAN
    else:
        filename += DATA_CANDIDATOS

    with open(filename) as json_file:  
        data = json.load(json_file)
    return data

def readCandidates(options):
    if options['from_notebook']:
        filename = '../' + DATA_CANDIDATOS_SIN_PARTIDO
    else:
        filename = DATA_CANDIDATOS_SIN_PARTIDO

    with open(filename) as json_file:  
        data = json.load(json_file)
    return data
            