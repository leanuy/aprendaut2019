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

# Estrategias de evaluación
class EvaluationOps(Enum):
    NORMAL = 1
    CROSS = 2

# Tipos de atributos
class AttributeType(Enum):
    DISCRETE = 0
    CONTINUOUS = 1

IRIS_DATASET = 'data/iris.arff'
COVERTYPE_DATASET = 'data/covertype.arff'