### DEPENDENCIAS
### ------------------

from enum import Enum

### CONSTANTES
### ------------------

# Opciones del menú principal
class MenuOps(Enum):
    TRAIN = 1
    PLAY = 2

# Tipos de jugadores para la opción JUGAR
class PlayerType(Enum):
    RANDOM = 1
    SELF = 2
    HUMAN = 3

# Tipos de juego para la clase Game
class GameMode(Enum):
    TRAINING = 1
    PLAYING = 2

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
