### DEPENDENCIAS
### ------------------

import sys
import os
import time

from model.training import Training
from model.model import Model

from game.game import Game
from game.player import Player

import utils.gui as gui
from utils.const import MenuOps, PlayerType, GameMode, GameTokens, GameResults

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.TRAIN
    players = []

    # NOTA: variable global con historial de models. Ver si rinde
    historial_weigths = []

    while op == MenuOps.TRAIN or op == MenuOps.PLAY:

        gui.printMenu(players)
        op = gui.printMenuOption()

        if op == MenuOps.TRAIN:

            (playerType, playerName) = gui.printPlayerType()
            iters = gui.printTrainingIterations()
            maxRounds = gui.printMaxRounds()
            learningRate = gui.printLearningRate()
            weights = gui.printInitialWeights()
            normalize_weights = gui.printNormalizeWeights()
            skip_on_draw = gui.printSkipOnDraw()

            print()
            print("-> COMIENZO DEL ENTRENAMIENTO")

            t = Training(GameTokens.PLAYER1, playerType, iters, learningRate, weights, maxRounds, normalize_weights, skip_on_draw)

            tic = time.time()
            (player, results) = t.training()
            toc = time.time()

            print("-> FIN DEL ENTRENAMIENTO")
            print()

            historial_weigths.append(player.getModel().getWeights())

            player = {
                'player': player,
                'type': playerType,
                'name': playerName,
                'time': toc-tic,
                'iterations': iters,
                'maxRounds': maxRounds,
                'learningRate': learningRate,
                'initialWeights': weights,
                'finalWeights': player.getModel().getWeights(),
                'results': results,
            }
            players.append(player)

            gui.printTrainedPlayer(player)
            input("-> Oprima enter para volver al menú")

        elif op == MenuOps.PLAY:

            gui.printClear()
            gui.printPlayers(players)

            c = int( input("-> Elija un jugador por el índice: ") )
            print("")

            if c >= 0 and c < len(players) + 1:

                # Representa la partida
                g = None

                # Se eligio un jugador aleatorio sin entrenar
                if c == 0:
                    g = Game(GameMode.PLAYING, Player(GameTokens.PLAYER1, PlayerType.RANDOM))

                # Se eligió un jugador previamente entrenado
                else:
                    g = Game(GameMode.PLAYING, players[c-1]['player'])

                # Se juega la partida y se imprime el mensaje segun el resultado
                res = g.play()
                if res == GameResults.WIN:
                    print("-> Has ganado la partida. Oprime enter para volver al menú")
                else:
                    print("-> Has perdido la partida. Oprime enter para volver al menú")
                input()
            else:
                print("-> El índice ingresado no corresponde a ningún jugador")