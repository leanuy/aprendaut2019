### DEPENDENCIAS
### ------------------

import math
import copy
import operator
import pandas as pd

from utils.const import AttributeType

### METODOS PRINCIPALES
### -------------------

# Lee 'filename' y lo devuelve como un dataframe de pandas optimizado
def readDataset(filename, is_for_pca=True):
    dataset = pd.read_csv(filename)

    if is_for_pca:
        solo_respuestas = dataset.iloc[1:, 2:28]
        return solo_respuestas


# Para el ejercicio 2, necesitamos obtener el partido segun el candidato del json. TBD
