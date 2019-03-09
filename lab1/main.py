### DEPENDENCIAS
### ------------------

import sys
import os
import time

from utils.const import MenuOps, PlayerType
from game.game import Game

### METODOS AUXILIARES
### ------------------

def printClear():
    if os.name == 'nt':
        clear = lambda : os.system('cls')
        clear()
    else:
        clear = lambda : os.system('clear')
        clear()

def printMenu(players):
    printClear()
    print ("#####################################################")
    print ("#                                                   #")
    print ("#        MENÚ - Laboratorio 1 (Damas Chinas)        #")
    print ("#                                                   #")
    print ("#####################################################")
    print ("")
    printPlayers(players)
    print ("1. Entrenar")
    print ("2. Jugar")
    print ("0. Salir")
def printMenuOption():
    print ("")   
    print ("-> Elija una opción: ")
    op = int( input() )

    if op < 1 or op > 2:
        sys.exit()
    else:
        if op == 1:
            op = MenuOps.TRAIN
        elif op == 2:
            op = MenuOps.PLAY

    return op

def printPlayers(players):
    if players == []:
        return
    else:
        print ("Jugadores actuales:")
        index = 0
        for p in players:
            print("-> ", end="")
            print(str(index), end="")
            print(" - ", end="")
            print("Jugador ", end="")
            print(p['name'])
            index = index + 1
        print ("")
def printPlayerType():
    print ("")
    print ("-> Elija un tipo de jugador para entrenar: ")
    print ("1. VS Random")
    print ("2. VS Si Mismo")
    playerType = int( input() )

    if playerType < 1 or playerType > 2:
        print("-> El primer argumento debe ser 1 o 2.")
        sys.exit()
    else:
        if playerType == 1:
            playerType = PlayerType.RANDOM
            playerName = "Random"
        elif playerType == 2:
            playerType = PlayerType.SELF
            playerName = "Si Mismo"

    return (playerType, playerName)

### METODO PRINCIPAL
### ----------------

if __name__ == '__main__':

    op = MenuOps.TRAIN
    players = []

    while op == MenuOps.TRAIN or op == MenuOps.PLAY:

        printMenu(players)
        op = printMenuOption()

        if op == MenuOps.TRAIN:

            (playerType, playerName) = printPlayerType()

            print()
            print("-> COMIENZO DEL ENTRENAMIENTO")

            tic = time.time()
            # Aca iniciamos el entrenamiento
            toc = time.time()

            print("-> FIN DEL ENTRENAMIENTO")
            print("--> Tiempo de entrenamiento: ", end="")
            print(toc-tic)

            player = {
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
                printClear()
                printPlayers(players)

                c = int( input("-> Elija un jugador por el índice: ") )
                print("")

                if c >= 0 and c < len(players):
                    g = Game()
                    g.play()
                else:
                    print("-> El índice ingresado no corresponde a ningún jugador")