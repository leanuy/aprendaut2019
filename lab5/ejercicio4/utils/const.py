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
    SEARCH = 4

class PlotOps(Enum):
    CORPUS = 1
    SINGLE = 2
    ALL = 3

class CandidateDivision(Enum):
    CANDIDATES = 0
    PARTIES = 1

class SolverOps(Enum):
    LIBLINEAR = "liblinear"
    LBFGS = "lbfgs"
    SAG = "sag"
    SAGA = "saga"
    NEWTON_CG = "newton-cg"

class PenaltyOps(Enum):
    L1 = 'l1'
    L2 = 'l2'

MaxIterOps = [100]
RegulationStrengthOps = [0.1, 1.0]

# Datasets y sus ubicaciones
DATA_ENCUESTAS = 'data/data.csv'
DATA_CANDIDATOS = 'data/candidatos.json'
DATA_CANDIDATOS_ESPECTRO = 'data/candidatosEspectro.json'
DATA_CANDIDATOS_ESPECTRO_DUAL = 'data/candidatosEspectroDual.json'
DATA_CANDIDATOS_NOLAN = 'data/candidatosNolan.json'
DATA_CANDIDATOS_SIN_PARTIDO = 'data/candidatosSinPartido.json'


