### DEPENDENCIAS
### ------------------

from enum import Enum

### CONSTANTES
### ------------------

# Opciones del menú principal
class MenuOps(Enum):
    PCA = 1

# Tipos de atributos
class AttributeType(Enum):
    DISCRETE = 0
    CONTINUOUS = 1

# Datasets y sus ubicaciones
DATA_ENCUESTAS = 'data/data.csv'
CANDIDATOS = 'data/candidatos.json'

