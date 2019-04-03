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

# Estrategias de atributos continuos
class ContinuousOps(Enum):
    FIXED = 1
    VARIABLE = 2
    C45 = 3

# Tipos de medidas
class MeasureOps(Enum):
    GAIN = 1
    GAINRATIO = 2
    IMPURITYREDUCTION = 3

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