### DEPENDENCIAS
### ------------------

from .model import Model

from game.game import Game
from game.player import Player

from utils.const import PlayerType, GameMode, GameTokens

import copy

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

            # Obtener tableros del juego
            historial = g.getBoards()

            # Obtener model
            model = self.player.getModel()

            # Se arma la lista de pares [tablero, v_train]
            ejemplos_entrenamiento = []
            for tablero, sucesor_t in zip(historial, historial[1:]):
                features = tablero.getFeatures(GameTokens.PLAYER1)
                featuresSuccessor = sucesor_t.getFeatures(GameTokens.PLAYER1)
                ejemplos_entrenamiento.append([features, model.evaluate(featuresSuccessor)])

            # Reviso si gane o perdi para poner el ultimo v_train
            if res:
                v_entrenamiento = 1
                results[0] = results[0] + 1
            else:
                v_entrenamiento = 0
                results[1] = results[1] + 1

            ult_tablero = historial[-1]
            ejemplos_entrenamiento.append([ult_tablero, v_entrenamiento])

            new_model = copy.deepcopy(model)

            for t in ejemplos_entrenamiento:
                new_model.update(t[0], t[1], self.learningRate)

            # Set past experience to the player
            self.player.setModel(new_model)

            # Set experience to oponent if not Random oponent
            if self.oponent.getPlayerType != PlayerType.TRAINED_RANDOM:
                self.oponent.setModel(model)


        return (self.player, results, new_model.getWeights())

