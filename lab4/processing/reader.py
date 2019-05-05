### DEPENDENCIAS
### ------------------

import json
import pandas as pd

### METODOS PRINCIPALES
### -------------------

# Lee 'filename' y lo devuelve como un dataframe de pandas optimizado
def readDataset(filename, is_for_pca=True):
    dataset = pd.read_csv(filename)

    if is_for_pca:
        candidates = dataset.iloc[1:, 1]
        answers = dataset.iloc[1:, 2:28]
        return candidates.apply(pd.to_numeric, downcast='unsigned'), answers.apply(pd.to_numeric, downcast='unsigned')

# Lee 'filename' y lo devuelve como archivo JSON
def readParties(filename):
    with open(filename) as json_file:  
        data = json.load(json_file)
    return data
            