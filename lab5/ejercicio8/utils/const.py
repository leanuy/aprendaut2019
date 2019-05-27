### DEPENDENCIAS
### ------------------

from enum import Enum

### CONSTANTES
### ------------------

# Opciones del menú principal
class MenuOps(Enum):
    TRAIN = 1
    LOAD = 2
    SAVE = 3
    EVALUATE = 4
    COMPARE = 5
    PLAY_VS_IA = 6
    WATCH_IA_VS_IA = 7
    TOURNEY = 8
    
# Tipos de modelos
class ModelTypes(Enum):
    LINEAR = 1
    NEURAL = 2

# Tipos de jugadores para la opción JUGAR
class PlayerType(Enum):
    RANDOM = 0
    TRAINED_RANDOM = 1
    TRAINED_SELF = 2
    TRAINED_SHOWDOWN = 3

# Features de la capa de entrada en una red
class InputLayerTypes(Enum):
    METRICS = 1
    BOARD = 2

# Tipos de funciones de activacion
class ActivationFunctions(Enum):
    RELU = 'relu'
    SIGMOID = 'logistic'
    TANH = 'tanh'

# Tipos de juego para la clase Game
class GameMode(Enum):
    TRAINING = 1
    PLAYING = 2
    SPECTATING = 3

# Tipos de pieza para la clase Game y Board
class GameTokens(Enum):
    PLAYER1 = 1
    PLAYER2 = 2
    EMPTY = 0

# Tipos de errores al intentar mover una pieza, para la clase Game
class GameTokenMoves(Enum):
    VALID_MOVE = 0      # El token en FROM puede moverse a TO
    INVALID_MOVE = 1    # El token en FROM no puede llegar a TO
    TOKEN_FROM = 2      # La posición FROM no tiene un token del jugador
    TOKEN_TO = 3        # La posición TO esta ocupada por otro token
    INVALID_COORDS = 4  # La posición FROM o TO no existe en el tablero

# Tipos de resultado de una partida
class GameResults(Enum):
    WIN = 1
    LOSE = -1
    DRAW = 0

# Versores con direcciones de desplazamiento
AxialDirections = {
    'northwest': (0,-1),
    'west': (-1,0),
    'southwest': (-1,1),
    'southeast': (0,1),
    'east': (1,0),
    'northeast': (1,-1)
}

# Datasets y sus ubicaciones
DATA_BOARDS = 'data/boards.csv'
DATA_METRICS = 'data/metrics.csv'