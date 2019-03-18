### DEPENDENCIAS
### ------------------

import copy
import matplotlib.pyplot as plt

from .model import Model

from game.game import Game
from game.player import Player

from utils.const import PlayerType, GameMode, GameTokens, GameResults


### CLASE PRINCIPAL
### ------------------

class Training():

    ### METODOS AUXILIARES
    ### -------------------

    def saveModel(self):
        print("Guarda los pesos obtenidos del entrenamiento en un archivo de texto")

    def printPlot(self, x_axis, y_axis, iterations):
        plt.plot(x_axis, y_axis, 'ro')
        plt.axis([0, iterations - 1, -2, 2])
        plt.show()

    ### METODOS PRINCIPALES
    ### -------------------

    def __init__(self, playerToken, playerType, iters, learningRate, weights, maxRounds, normalize_weights, skip_on_draw):
        self.skip_on_draw = skip_on_draw

        # Guarda el numero de ficha del jugador y de su oponente
        self.playerToken = playerToken
        self.opponentToken = None
        if playerToken == GameTokens.PLAYER1:
            self.opponentToken = GameTokens.PLAYER2
        else:
            self.opponentToken = GameTokens.PLAYER1

        # Crea al jugador a entrenar y su respectivo modelo
        self.player = Player(self.playerToken, playerType, Model(normalize_weights, weights))
        
        # Crea al oponente y su respectivo modelo en base al playerType, es decir
        # al tipo de jugador que se quiere entrenar
        self.opponent = None
        if playerType == PlayerType.TRAINED_RANDOM:
            self.opponent = Player(self.opponentToken, PlayerType.RANDOM)
        elif playerType == PlayerType.TRAINED_SELF:
            self.opponent = Player(self.opponentToken, PlayerType.TRAINED_SELF, Model(normalize_weights, weights))

        # Tipo de jugador a entrenar (basado en su oponente)
        self.playerType = playerType

        # Cantidad de iteraciones en el entrenamiento
        self.iters = iters

        # Ratio de aprendizaje en el entrenamiento
        self.learningRate = learningRate

        # Cantidad de turnos antes de declarar empate
        self.maxRounds = maxRounds

    # Entrenamiento del modelo
    def training(self):

        results = [0,0,0]
        x_axis = []
        y_axis = []

        variable = self.learningRate == 'var'

        if variable:
            self.learningRate = 1
            count = 100
        
        i = 0
        while i < self.iters:
            if variable:
                # print("Iteracion numero: ", str(i))
                if count != 100 and count % 10 == 0:
                    self.learningRate -= 0.1
                    # print("Learning rate = ", str(self.learningRate))
            
            # Se genera un juego nuevo para cada iteración
            g = Game(GameMode.TRAINING, (self.player, self.opponent), self.maxRounds)
            res = g.play()

            # Obtener tableros del juego
            historial = g.getBoards()

            # Obtener model
            model = self.player.getModel()

            # Se arma la lista de pares [tablero, evaluación de sucesor]
            trainingExamples = []
            for board, nextBoard in zip(historial, historial[1:]):
                features = board.getFeatures(self.playerToken)
                nextFeatures = nextBoard.getFeatures(self.playerToken)
                trainingExamples.append([features, model.evaluate(nextFeatures)])

            # Se checkea el resultado del juego para setear la evaluación
            # del último tablero
            if res == GameResults.WIN:
                lastEvaluation = 1
                results[0] = results[0] + 1
            elif res == GameResults.LOSE:
                lastEvaluation = -1
                results[1] = results[1] + 1
            else:
                results[2] = results[2] + 1
                if not self.skip_on_draw:
                    print("Resultado omitido a causa de empate")
                    i += 1
                    if variable:
                        count -= 1
                    continue
                lastEvaluation = 0

            x_axis.append(i)
            y_axis.append(lastEvaluation)
            
            lastBoard = historial[-1]
            trainingExamples.append([lastBoard.getFeatures(self.playerToken), lastEvaluation])

            # Se realiza una copia del modelo actual para que el oponente use
            # en la próxima iteración (a menos que sea oponente random)
            new_model = copy.deepcopy(model)

            # Se actualizan los pesos del modelo utilizando los datos de la
            # última partida
            for t in trainingExamples:
                new_model.update(t[0], t[1], self.learningRate)
            self.player.setModel(new_model)

            # Se sustituye el modelo del oponente por el modelo utilizado en
            # esta partida antes de actualizar los pesos
            if self.opponent.getPlayerType() != PlayerType.TRAINED_RANDOM:
                self.opponent.setModel(model)

            i += 1
            if variable:
                count -= 1
        self.printPlot(x_axis, y_axis, self.iters)
        
        return (self.player, results)

