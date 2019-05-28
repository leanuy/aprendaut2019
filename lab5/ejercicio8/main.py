### DEPENDENCIAS
### ------------------

import sys
import os
import time
import copy

from model.training import Training
from model.training_duel import TrainingDuel
from model.model_concept import ModelConcept
from game.game import Game
from game.player import Player
import evaluation.evaluator as evaluator
import processing.plotter as plotter
import processing.archiver as archiver
import utils.gui as gui
from utils.const import MenuOps, PlayerType, GameMode, GameTokens, GameResults, ModelTypes, PlayerType, ArchiveOps

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.TRAIN
    players = []

    # NOTA: variable global con historial de models. Ver si rinde
    historial_weigths = []

    while op == MenuOps.TRAIN or op == MenuOps.LOAD or op == MenuOps.SAVE or op == MenuOps.EVALUATE or op == MenuOps.SEARCH or op == MenuOps.COMPARE or op == MenuOps.PLAY_VS_IA or op == MenuOps.WATCH_IA_VS_IA or op == MenuOps.TOURNEY:

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

                if modelType == ModelTypes.NEURAL:
                    options = {
                        'playerType': playerType,
                        'modelType': modelType,
                        'inputLayer': gui.printInputLayer(),
                        'hiddenLayer': gui.printHiddenLayers(),
                        'hiddenNeuron': gui.printHiddenNeurons(),
                        'activationFunction': gui.printActivationFunction(),
                        'learningRate': gui.printLearningRateNeural(),
                        'iters': gui.printTrainingIterations(),
                        'maxRounds': gui.printMaxRounds(),
                        'notDraw': gui.printSkipOnDraw(),
                    }
                    options['hiddenLayerSizes'] = tuple([options['hiddenNeuron'] for i in range(options['hiddenLayer'])])

                else:
                    options = {
                        'playerType': playerType,
                        'modelType': modelType,
                        'weights': gui.printInitialWeights(),
                        'normalize_weights': gui.printNormalizeWeights(),
                        'learningRate': gui.printLearningRate(),
                        'iters': gui.printTrainingIterations(),
                        'maxRounds': gui.printMaxRounds(),
                        'notDraw': gui.printSkipOnDraw(),
                    }
                
                t = Training(GameTokens.PLAYER1, options)

                print()
                print("-> COMIENZO DEL ENTRENAMIENTO")

                tic = time.time()
                (player, results, resultsPlot, errorsPlot) = t.training()
                toc = time.time()

                print("-> FIN DEL ENTRENAMIENTO")
                print()

                if modelType == ModelTypes.NEURAL:
                    playerData = {
                        'player': player,
                        'type': playerType,
                        'name': modelName,
                        'modelType': modelType,
                        'time': toc-tic,
                        'inputLayer': options['inputLayer'],
                        'hiddenLayer': options['hiddenLayer'],
                        'hiddenNeuron': options['hiddenNeuron'],
                        'activationFunction': options['activationFunction'],
                        'learningRate': options['learningRate'],
                        'iterations': options['iters'],
                        'maxRounds': options['maxRounds'],
                        'notDraw': options['notDraw'],
                        'results': results
                    }

                else:
                    playerData = {
                        'player': player,
                        'type': playerType,
                        'name': modelName,
                        'modelType': modelType,
                        'time': toc-tic,
                        'initialWeights': options['weights'],
                        'finalWeights': player.getModel().getWeights(),
                        'normalize_weights': options['normalize_weights'],
                        'learningRate': options['learningRate'],
                        'iterations': options['iters'],
                        'maxRounds': options['maxRounds'],
                        'notDraw': options['notDraw'],
                        'results': results
                    }
                    historial_weigths.append(player.getModel().getWeights())

                players.append(playerData)
                gui.printTrainedPlayer(playerData)
                plotter.printResultsPlot(resultsPlot, options['iters'])
                
                if modelType == ModelTypes.LINEAR:
                    plotter.printErrorPlot(errorsPlot, options['iters'])

                filename = gui.printSavePlayer()
                archiver.savePlayer(filename, playerData)

            input("-> Oprima enter para volver al menú")

        elif op == MenuOps.LOAD:
            archive_op = gui.printArchiveOptions(ArchiveOps.LOAD)
            if archive_op == ArchiveOps.SINGLE:
                filename = gui.printLoadPlayer()
                p = archiver.loadPlayer(filename)
                if p != None:
                    players.append(p)
            else:
                fileprefix = gui.printLoadMassive()
                players = archiver.loadMassive(fileprefix)

            input("-> Oprima enter para volver al menú")

        elif op == MenuOps.SAVE:
            archive_op = gui.printArchiveOptions(ArchiveOps.LOAD)
            playerIndex = gui.pickPlayer(players)
            player = players[playerIndex-1]
            filename = gui.printSavePlayer()
            archiver.savePlayer(filename, player)

            input("-> Oprima enter para volver al menú")
            
        elif op == MenuOps.SEARCH:

            playerType = gui.printPlayerType(False)
            inputLayer = gui.printInputLayer()

            players = evaluator.getAllNeuralNetworks(playerType, inputLayer)
            sortedPlayers = evaluator.getBestNeuralNetworks(players)

            print('El mejor modelo es: ')
            gui.printTrainedPlayer(sortedPlayers[0], players.index(sortedPlayers[0]) + 1)

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