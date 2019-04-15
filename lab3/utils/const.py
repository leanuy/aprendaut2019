### DEPENDENCIAS
### ------------------

from enum import Enum

### CONSTANTES
### ------------------

# Opciones del menú principal
class MenuOps(Enum):
    TRAIN = 1
    CLASSIFY = 2    
    EVALUATE = 3
    SHOW = 4

# Opciones del tipo de modelo
class ModelOps(Enum):
    DECISION_TREE = 1
    DECISION_FOREST = 2
    NAIVE_BAYES = 3
    KNN = 4

# Estrategias de atributos continuos
class ContinuousOps(Enum):
    FIXED = 1
    VARIABLE = 2
    C45 = 3
    STANDARDIZATION = 4

# Tipos de medidas
class MeasureOps(Enum):
    GAIN = 1
    GAINRATIO = 2
    IMPURITYREDUCTION = 3

# Tipos de distancias
class DistanceOps(Enum):
    MANHATTAN = 1
    EUCLIDEAN = 2
    CHEBYCHEV = 3
    MAHALANOBIS = 4

DistanceMetrics = {
    DistanceOps.MANHATTAN: 'manhattan',
    DistanceOps.EUCLIDEAN: 'euclidean',
    DistanceOps.CHEBYCHEV: 'chebyshev',
    DistanceOps.MAHALANOBIS: 'mahalanobis',
}

# Estrategias de normalización
class NormOps(Enum):
    NONE = 0
    EUCLIDEAN = 1
    MIN_MAX = 2
    Z_SCORE = 3

# Estrategias de evaluación
class EvaluationOps(Enum):
    NORMAL = 1
    CROSS = 2

# Tipos de atributos
class AttributeType(Enum):
    DISCRETE = 0
    CONTINUOUS = 1

# Configuraciones paramétricas de entrenamiento
CONTINUOUS = 'continuous'
MEASURE = 'measure'

# Datasets y sus ubicaciones
IRIS_DATASET = 'data/iris.arff'
COVERTYPE_DATASET = 'data/covertype.arff'