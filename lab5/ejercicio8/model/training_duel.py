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

class TrainingDuel():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, player1, player2, options):

        # Tipo de jugador a entrenar (basado en su oponente)
        self.playerType = options['playerType']

        # Cantidad de iteraciones en el entrenamiento
        self.iters = options['iters']

        # Cantidad de turnos antes de declarar empate
        self.maxRounds = options['maxRounds']

        self.notDraw = options['notDraw']

        # Ratio de aprendizaje en el entrenamiento
        self.learningRate = options['learningRate']

        self.spectate = options['spectate']

        self.player1 = player1

        self.player2 = player2

    # Entrenamiento de los modelos
    def training(self):
        results = [0,0,0]
        results_x_axis = []
        results_y_axis = []
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
            g = Game(GameMode.TRAINING, (self.player1, self.player2), self.maxRounds)
            res = g.play(self.spectate)

            # Obtener tableros del juego
            historial = g.getBoards()

            # Se checkea el resultado del juego para setear la evaluación del último tablero
            if res == GameResults.WIN:
                print("-> Ha ganado el jugador 1!")
                lastEvaluation = 1
                results[0] = results[0] + 1
            elif res == GameResults.LOSE:
                print("-> Ha ganado el jugador 2!")
                lastEvaluation = -1
                results[1] = results[1] + 1
            else:
                print("-> Ha habido un empate!")
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
            if self.player1.getPlayerType() != PlayerType.TRAINED_RANDOM:
                # Entrenamiento del player 1
                trainingExamplesPlayer1 = self.getTrainingExamples(self.player1, historial, lastEvaluation)

            if self.player2.getPlayerType() != PlayerType.TRAINED_RANDOM:
                # Entrenamiento del player 2
                if lastEvaluation == 1:
                    lastEvaluation = -1
                trainingExamplesPlayer2 = self.getTrainingExamples(self.player2, historial, lastEvaluation)
   
            # Se actualizan los pesos del modelo utilizando los datos de la última partida

            # Player 1
            if self.player1.getPlayerType() != PlayerType.TRAINED_RANDOM:
                self.updatePlayer(self.player1, trainingExamplesPlayer1)

            # Player2
            if self.player2.getPlayerType() != PlayerType.TRAINED_RANDOM:
                self.updatePlayer(self.player2, trainingExamplesPlayer2)

            i += 1
            if variable:
                count -= 1

        return (self.player1, self.player2, results, (results_x_axis, results_y_axis))
    
    def getTrainingExamples(self, player, historial, lastEvaluation):
        # Se arma la lista de pares [tablero, evaluación de sucesor]
        trainingExamples = []
        if player.model.options['modelType'] == ModelTypes.LINEAR:
            for board, nextBoard in zip(historial, historial[1:]):
                features = board.getFeatures(player.playerNumber)
                nextFeatures = nextBoard.getFeatures(player.playerNumber)
                trainingExamples.append([features, player.model.evaluate(nextFeatures)])
            lastBoard = historial[-1]
            trainingExamples.append([lastBoard.getFeatures(player.playerNumber), lastEvaluation])
        else: # Neural
            boardIndex = 0
            for board in reversed(historial):
                trainingExamples.append([board.getFeatures(player.playerNumber, player.model.options['inputLayer']), pow(0.9,boardIndex)*lastEvaluation])
                boardIndex += 1
        return trainingExamples
    
    def updatePlayer(self, player, trainingExamples):
        if player.model.options['modelType'] == ModelTypes.LINEAR:
            index = 0
            for t in trainingExamples:
                player.model.update(t[0], t[1], self.learningRate)
                player.model.update(t[0], t[1], self.learningRate)
                index += 1
        else: # Neural
            trainingExamples = np.array(trainingExamples)
            player.model.update(trainingExamples[:,0], trainingExamples[:,1])