### DEPENDENCIAS
### ------------------

from .model import Model

from game.game import Game
from game.player import Player

from utils.const import PlayerType, GameMode, GameTokens

### CLASE PRINCIPAL
### ------------------

class Training():

    ### METODOS AUXILIARES
    ### -------------------

    def saveModel(self):
        print("Guarda los pesos obtenidos del entrenamiento en un archivo de texto")

    ### METODOS PRINCIPALES
    ### -------------------

    def __init__(self, playerType, iters, learningRate, weights):

        # Crea al jugador a entrenar y su respectivo modelo
        self.player = Player(GameTokens.PLAYER1, playerType, Model(weights))
        
        # Crea al oponente y su respectivo modelo en base al playerType, es decir
        # al tipo de jugador que se quiere entrenar
        self.opponent = None
        if playerType == PlayerType.TRAINED_RANDOM:
            self.opponent = Player(GameTokens.PLAYER2 ,PlayerType.RANDOM)
        elif playerType == PlayerType.TRAINED_SELF:
            self.opponent = Player(GameTokens.PLAYER2, PlayerType.TRAINED_SELF, Model(weights))

        # Tipo de jugador a entrenar (basado en su oponente)
        self.playerType = playerType

        # Cantidad de iteraciones en el entrenamiento
        self.iters = iters

        # Ratio de aprendizaje en el entrenamiento
        self.learningRate = learningRate

    # Entrenamiento del modelo
    def training(self):

        results = [0,0,0]

        for i in range(0, self.iters):

            g = Game(GameMode.TRAINING, (self.player, self.opponent))
            res = g.play()

            if res:
                results[0] = results[0] + 1
            else:
                results[1] = results[1] + 1

            # Aca va el codigo de actualizar los pesos

        return (self.player, results)

