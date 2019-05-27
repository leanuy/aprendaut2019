### DEPENDENCIAS
### ------------------

import sys
import os
import time
import pickle
import copy

from model.training import Training
from model.training_duel import TrainingDuel
from model.model_concept import ModelConcept

from game.game import Game
from game.player import Player

import utils.gui as gui
import processing.plotter as plotter
from utils.const import MenuOps, PlayerType, GameMode, GameTokens, GameResults, ModelTypes, PlayerType


### MÉTOTODOS AUXILIARES
### --------------------

def savePlayer(player):
    filename = gui.printSavePlayer()
    if filename.strip():
        root = 'players/'
        filename = root + filename
        pickle_out = open(filename,"wb")
        pickle.dump(player, pickle_out)
        pickle_out.close()

def loadPlayer():
    filename = gui.printLoadPlayer()
    if filename.strip():
        root = 'players/'
        filename = root + filename
        try:
            pickle_in = open(filename,"rb")
            loaded_player = pickle.load(pickle_in)

            # Ajuste del nombre
            modelName = gui.getModelName(loaded_player['modelType'])
            index = 0
            for player in players:
                if (player['modelType'] is not None) and (player['modelType'] == loaded_player['modelType']):
                    index += 1
            playerName = f'{modelName} - {index}'
            loaded_player['name'] = playerName

            players.append(loaded_player)
        except:
            print("Error! Archivo erroneo, por favor intente nuevamente.")
            input()


### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.TRAIN
    players = []

    # NOTA: variable global con historial de models. Ver si rinde
    historial_weigths = []

    while op == MenuOps.TRAIN or op == MenuOps.PLAY_VS_IA or op == MenuOps.LOAD or op == MenuOps.WATCH_IA_VS_IA or op == MenuOps.SAVE:

        gui.printMenu(players)
        op = gui.printMenuOption()

        if op == MenuOps.TRAIN:
            playerType = gui.printPlayerType()

            if playerType == PlayerType.TRAINED_SHOWDOWN:
                player1Index = gui.pickPlayer(players, "-> Elija al jugador 1 por su índice: ")
                player2Index = gui.pickPlayer(players, "-> Elija al jugador 2 por su índice: ")
                
                player = players[player1Index-1]['player']
                player1 = Player(GameTokens.PLAYER1, player.playerType, copy.deepcopy(player.model))

                player = players[player2Index-1]['player']
                player2 = Player(GameTokens.PLAYER2, player.playerType, copy.deepcopy(player.model))

                spectate = gui.printSpectateOptions()

                options = {
                    'playerType': playerType,
                    'iters': gui.printTrainingIterations(),
                    'maxRounds': gui.printMaxRounds(),
                    'notDraw': gui.printSkipOnDraw(),
                    'learningRate': gui.printLearningRate(),
                    'spectate': spectate
                }

                t = TrainingDuel(player1, player2, options)

                (player1, player2, results, resultsPlot) = t.training()

                # Updateamos los modelos
                players[player1Index-1]['player'] = player1

                # HACK: Guardamos a player1 como un player1 para que no se rompa play vs AI.
                player2.setPlayerNumber(GameTokens.PLAYER1)
                players[player2Index-1]['player'] = player2

                plotter.printResultsPlot(resultsPlot, options['iters'])
                
            # Normal training
            else:
                (modelType, modelName) = gui.printModelOptions()

                index = 0
                for player in players:
                    if player['modelType'] is not None and player['modelType'] == modelType:
                        index += 1
                playerName = f'{modelName} - {index}'

                options = {
                    'modelType': modelType,
                    'playerType': playerType,
                    'iters': gui.printTrainingIterations(),
                    'maxRounds': gui.printMaxRounds(),
                    'notDraw': gui.printSkipOnDraw(),
                    'learningRate': 1
                }
                if modelType == ModelTypes.LINEAR:
                    options['weights'] = gui.printInitialWeights()
                    options['normalize_weights'] = gui.printNormalizeWeights()
                    options['learningRate'] = gui.printLearningRate()
                
                t = Training(GameTokens.PLAYER1, options)

                print()
                print("-> COMIENZO DEL ENTRENAMIENTO")

                tic = time.time()
                (player, results, resultsPlot, errorsPlot) = t.training()
                toc = time.time()

                print("-> FIN DEL ENTRENAMIENTO")
                print()

                playerData = {
                    'player': player,
                    'type': playerType,
                    'modelType': modelType,
                    'name': playerName,
                    'time': toc-tic,
                    'iterations': options['iters'],
                    'maxRounds': options['maxRounds'],
                    'results': results,
                    'learningRate': options['learningRate']
                }
                if modelType == ModelTypes.LINEAR:
                    historial_weigths.append(player.getModel().getWeights())
                    playerData['initialWeights'] = options['weights']
                    playerData['finalWeights'] = player.getModel().getWeights()

                players.append(playerData)

                gui.printTrainedPlayer(playerData)
                plotter.printResultsPlot(resultsPlot, options['iters'])
                if modelType == ModelTypes.LINEAR:
                    plotter.printErrorPlot(errorsPlot, options['iters'])

                savePlayer(playerData)

            input("-> Oprima enter para volver al menú")

        elif op == MenuOps.PLAY_VS_IA:

            player = gui.pickPlayer(players)

            # Representa la partida
            g = None

            # Se eligio un jugador aleatorio sin entrenar
            if player == 0:
                g = Game(GameMode.PLAYING, Player(GameTokens.PLAYER1, PlayerType.RANDOM))

            # Se eligió un jugador previamente entrenado
            else:
                g = Game(GameMode.PLAYING, players[player-1]['player'])

            # Se juega la partida y se imprime el mensaje segun el resultado
            res = g.play()
            if res == GameResults.WIN:
                print("-> Has ganado la partida. Oprime enter para volver al menú")
            else:
                print("-> Has perdido la partida. Oprime enter para volver al menú")
            input()

        elif op == MenuOps.WATCH_IA_VS_IA:
            player1Index = gui.pickPlayer(players, "-> Elija al jugador 1 por su índice: ")
            player2Index = gui.pickPlayer(players, "-> Elija al jugador 2 por su índice: ")
            
            # Representa la partida
            g = None

            # Se eligio un jugador aleatorio sin entrenar
            if player1Index == 0:
                player1 = Player(GameTokens.PLAYER1, PlayerType.RANDOM)
            else:
                player = players[player1Index-1]['player']
                player1 = Player(GameTokens.PLAYER1, player.playerType, copy.deepcopy(player.model))
            
            if player2Index == 0:
                player2 = Player(GameTokens.PLAYER2, PlayerType.RANDOM)
            else:
                player = players[player2Index-1]['player']
                player2 = Player(GameTokens.PLAYER2, player.playerType, copy.deepcopy(player.model))

            g = Game(GameMode.SPECTATING, (player1, player2))

            # Se juega la partida y se imprime el mensaje segun el resultado
            res = g.play(True)
            if res == GameResults.WIN:
                print("-> Ha ganado el jugador 1! Oprime enter para volver al menú")
            elif res == GameResults.LOSE:
                print("-> Ha ganado el jugador 2! Oprime enter para volver al menú")
            else:
                print("-> Ha habido un empate! Oprime enter para volver al menú")
            input()

        elif op == MenuOps.LOAD:
            loadPlayer()

        elif op == MenuOps.SAVE:
            playerIndex = gui.pickPlayer(players)
            player = players[playerIndex-1]
            savePlayer(player)
            