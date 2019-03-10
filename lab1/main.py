### DEPENDENCIAS
### ------------------

import sys
import os
import time

import utils.gui as gui
from utils.const import MenuOps, PlayerType, GameMode, GameTokens

from model.training import Training
from game.game import Game
from game.player import Player

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

            print()
            print("-> COMIENZO DEL ENTRENAMIENTO")

            t = Training()
            tic = time.time()
            t.training()
            toc = time.time()

            print("-> FIN DEL ENTRENAMIENTO")
            print("--> Tiempo de entrenamiento: ", end="")
            print(toc-tic)

            player = {
                'player': Player(GameTokens.PLAYER1, playerType),
                'type': playerType,
                'name': playerName,
                'time': toc-tic,
            }
            players.append(player)

            print()
            input("-> Oprima enter para volver al menú")

        elif op == MenuOps.PLAY:

            if players == []:
                print()
                print ("-> No hay jugadores, entrene uno para jugar")
                input("-> Oprima enter para volver al menú")
            else:
                gui.printClear()
                gui.printPlayers(players)

                c = int( input("-> Elija un jugador por el índice: ") )
                print("")

                if c >= 0 and c < len(players):
                    g = Game(GameMode.PLAYING, players[c]['player'])
                    g.play()
                else:
                    print("-> El índice ingresado no corresponde a ningún jugador")