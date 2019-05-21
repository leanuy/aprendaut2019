### DEPENDENCIAS
### ------------------

from enum import Enum

### CONSTANTES
### ------------------

# Opciones del menú principal
class MenuOps(Enum):
    TRAIN = 1
    EVALUATE = 2
    PLOT = 3

class SolverOps(Enum):
    LIBLINEAR = "liblinear"
    LBFGS = "lbfgs"
    SAG = "sag"
    SAGA = "saga"
    NEWTON_CG = "newton-cg"

class PenaltyOps(Enum):
    NONE = 'None'
    L1 = 'l1'
    L2 = 'l2'
    ELASTICNET = 'elasticnet'

class CandidateDivision(Enum):
    CANDIDATES = 0
    PARTIES = 1

# Datasets y sus ubicaciones
DATA_ENCUESTAS = 'data/data.csv'
DATA_CANDIDATOS = 'data/candidatos.json'
DATA_CANDIDATOS_ESPECTRO = 'data/candidatosEspectro.json'
DATA_CANDIDATOS_ESPECTRO_DUAL = 'data/candidatosEspectroDual.json'
DATA_CANDIDATOS_NOLAN = 'data/candidatosNolan.json'
DATA_CANDIDATOS_SIN_PARTIDO = 'data/candidatosSinPartido.json'


