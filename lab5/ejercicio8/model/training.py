### DEPENDENCIAS
### ------------------

import csv
import copy
import matplotlib.pyplot as plt
import numpy as np

from .model_concept import ModelConcept
from .model_neural import ModelNeural

from game.game import Game
from game.player import Player

from utils.const import PlayerType, GameMode, GameTokens, GameResults, ModelTypes


### CLASE PRINCIPAL
### ------------------

class Training():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, playerToken, options):

        self.modelType = options['modelType']

        # Tipo de jugador a entrenar (basado en su oponente)
        self.playerType = options['playerType']

        # Cantidad de iteraciones en el entrenamiento
        self.iters = options['iters']

        # Cantidad de turnos antes de declarar empate
        self.maxRounds = options['maxRounds']

        self.notDraw = options['notDraw']

        # Ratio de aprendizaje en el entrenamiento
        self.learningRate = options['learningRate']

        # Guarda el numero de ficha del jugador y de su oponente
        self.playerToken = playerToken
        if playerToken == GameTokens.PLAYER1:
            self.opponentToken = GameTokens.PLAYER2
        else:
            self.opponentToken = GameTokens.PLAYER1

        if self.modelType == ModelTypes.LINEAR:
            # Crea al jugador a entrenar y su respectivo modelo
            self.player = Player(self.playerToken, self.playerType, ModelConcept(options))
        else:
            self.player = Player(self.playerToken, self.playerType, ModelNeural(options, self.playerToken))

        # Crea al oponente y su respectivo modelo en base al playerType, (al tipo de jugador que se quiere entrenar)
        if self.playerType == PlayerType.TRAINED_RANDOM:
            self.opponent = Player(self.opponentToken, PlayerType.RANDOM)
        elif self.playerType == PlayerType.TRAINED_SELF:
            if self.modelType == ModelTypes.LINEAR:
                self.opponent = Player(self.opponentToken, PlayerType.TRAINED_SELF, ModelConcept(options))
            else:
                self.opponent = Player(self.opponentToken, PlayerType.TRAINED_SELF, ModelNeural(options, self.opponentToken))

    # Entrenamiento del modelo
    def training(self):
        results = [0,0,0]
        results_x_axis = []
        results_y_axis = []
        errors = []
        variable = self.learningRate == 'var'

        if variable:
            self.learningRate = 1
            count = 100

        i = 0
        while i < self.iters:
            if variable:
                if count != 100 and count % 10 == 0:
                    self.learningRate -= 0.1
            
            # Se genera un juego nuevo para cada iteración
            g = Game(GameMode.TRAINING, (self.player, self.opponent), self.maxRounds)
            res = g.play()

            # Obtener tableros del juego
            historial = g.getBoards()

            # Obtener model
            model = self.player.getModel()

            # Se checkea el resultado del juego para setear la evaluación del último tablero
            if res == GameResults.WIN:
                lastEvaluation = 1
                results[0] = results[0] + 1
            elif res == GameResults.LOSE:
                lastEvaluation = -1
                results[1] = results[1] + 1
            else:
                results[2] = results[2] + 1
                if not self.notDraw:
                    print("Resultado omitido a causa de empate")
                    i += 1
                    if variable:
                        count -= 1
                    continue
                lastEvaluation = -0.5
            results_x_axis.append(i)
            if lastEvaluation == -0.5:
                results_y_axis.append(0)
            else:
                results_y_axis.append(lastEvaluation)

            # Se arma la lista de pares [tablero, evaluación de sucesor]
            trainingExamples = []
            if self.modelType == ModelTypes.LINEAR:
                for board, nextBoard in zip(historial, historial[1:]):
                    features = board.getFeatures(self.playerToken, self.modelType)
                    nextFeatures = nextBoard.getFeatures(self.playerToken, self.modelType)
                    trainingExamples.append([features, model.evaluate(nextFeatures)])
                lastBoard = historial[-1]
                trainingExamples.append([lastBoard.getFeatures(self.playerToken, self.modelType), lastEvaluation])
            else: # Neural
                boardIndex = 0
                for board in reversed(historial):
                    trainingExamples.append([board.getFeatures(self.playerToken, self.modelType), pow(0.9,boardIndex)*lastEvaluation])
                    boardIndex += 1

            # Se realiza una copia del modelo actual para que el oponente use
            # en la próxima iteración (a menos que sea oponente random)
            new_model = copy.deepcopy(model)

            errors.append(([], []))
            (error_x_axis, error_y_axis) = errors[-1]

            # Se actualizan los pesos del modelo utilizando los datos de la última partida
            if self.modelType == ModelTypes.LINEAR:
                index = 0
                for t in trainingExamples:
                    new_model.update(t[0], t[1], self.learningRate)
                    mse = new_model.update(t[0], t[1], self.learningRate)
                    index += 1
                    error_x_axis.append(index)
                    error_y_axis.append(mse)
            else: # Neural
                trainingExamples = np.array(trainingExamples)
                new_model.update(trainingExamples[:,0], trainingExamples[:,1])
            
            self.player.setModel(new_model)

            # Se sustituye el modelo del oponente por el modelo utilizado en
            # esta partida antes de actualizar los pesos
            if self.opponent.getPlayerType() != PlayerType.TRAINED_RANDOM:
                self.opponent.setModel(model)

            i += 1
            if variable:
                count -= 1

        return (self.player, results, (results_x_axis, results_y_axis), errors)

    def recordBoards(self, trainingExamples, historial):
        with open(r'metrics.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for t in trainingExamples:
                fieldsMetrics = t[0]
                fieldsMetrics= np.append(fieldsMetrics, t[1])
                writer.writerow(fieldsMetrics)
            writer.writerow([])
        with open(r'boards.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for i, board in enumerate(historial):
                fieldsBoard = board.getBoard()
                fieldsBoard = np.append(fieldsBoard, trainingExamples[i][1])
                writer.writerow(fieldsBoard)
            writer.writerow([])
