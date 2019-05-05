### DEPENDENCIAS
### ------------------

from enum import Enum

### CONSTANTES
### ------------------

# Opciones del menú principal
class MenuOps(Enum):
    PCA = 1
    KMEANS = 2

class PCAOps(Enum):
    COVARIANZA = 0
    SVD = 1

class PCAnalysis(Enum):
    GENERAL = 0
    ALL_PARTY = 1
    EACH_PARTY = 2

# Datasets y sus ubicaciones
DATA_ENCUESTAS = 'data/data.csv'
DATA_CANDIDATOS = 'data/candidatos.json'

