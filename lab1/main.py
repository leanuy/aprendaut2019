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
from utils.const import MenuOps, PlayerType, GameMode, GameTokens

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.TRAIN
    players = []

    while op == MenuOps.TRAIN or op == MenuOps.PLAY:

        gui.printMenu(players)
        op = gui.printMenuOption()

        if op == MenuOps.TRAIN:

            (playerType, playerName) = gui.printPlayerType()
            iters = gui.printTrainingIterations()
            learningRate = gui.printLearningRate()
            weights = gui.printInitialWeights()

            print()
            print("-> COMIENZO DEL ENTRENAMIENTO")

            t = Training(playerType, iters, learningRate, weights)

            tic = time.time()
            player = t.training()
            toc = time.time()

            print("-> FIN DEL ENTRENAMIENTO")
            print("--> Tiempo de entrenamiento: ", end="")
            print(toc-tic)

            player = {
                'player': player,
                'type': playerType,
                'name': playerName,
                'time': toc-tic,
                'iterations': iters,
                'learningRate': learningRate,
                'initialWeights': weights,
            }
            players.append(player)

            print()
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
                if res:
                    print("-> Has ganado la partida. Oprime enter para volver al menú")
                else:
                    print("-> Has perdido la partida. Oprime enter para volver al menú")
                input()
            else:
                print("-> El índice ingresado no corresponde a ningún jugador")