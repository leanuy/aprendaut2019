### DEPENDENCIAS
### ------------------

from enum import Enum

### CONSTANTES
### ------------------

# Opciones del menú principal
class MenuOps(Enum):
    LOGISTIC_REGRESSION = 1
    PCA = 2

class SOLVEROps(Enum):
    LIBLINEAR = "liblinear"
    LBFGS = "lbfgs"
    SAG = "sag"
    SAGA = "saga"
    NEWTON_CG = "newton-cg"

class PENALTYOps(Enum):
    NONE = 'None'
    L1 = 'l1'
    L2 = 'l2'
    ELASTICNET = 'elasticnet'

class PCAOps(Enum):
    COVARIANZA = 0
    SVD = 1

class PCAnalysis(Enum):
    NONE = 0
    GENERAL = 1
    ALL_PARTY = 2
    EACH_PARTY = 3

class PCAIntermediates(Enum):
    NONE = 0
    COV_MATRIX = 1    
    EIGEN_VALUES = 2
    VARIANCE_RATIO = 3

class KmeansAnalysis(Enum):
    NONE = 0
    GENERAL = 1
    CANDIDATES = 2
    PARTIES = 3

class KmeansEvaluations(Enum):
    NONE = 0
    SILHOUETTE = 1
    ARI = 2

class CandidateDivision(Enum):
    PARTIES = 0
    SPECTRUM = 1
    NOLAN = 2
    DUAL_SPECTRUM = 3

# Datasets y sus ubicaciones
DATA_ENCUESTAS = 'data/data.csv'
DATA_CANDIDATOS = 'data/candidatos.json'
DATA_CANDIDATOS_ESPECTRO = 'data/candidatosEspectro.json'
DATA_CANDIDATOS_ESPECTRO_DUAL = 'data/candidatosEspectroDual.json'
DATA_CANDIDATOS_NOLAN = 'data/candidatosNolan.json'
DATA_CANDIDATOS_SIN_PARTIDO = 'data/candidatosSinPartido.json'


