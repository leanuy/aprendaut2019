### DEPENDENCIAS
### ------------------

import os
import sys
from termcolor import colored, cprint

from .const import MenuOps, PlayerType, GameMode, GameTokens

### METODOS AUXILIARES - MENU
### -------------------------

# Limpia la consola
def printClear():
    if os.name == 'nt':
        clear = lambda : os.system('cls')
        clear()
    else:
        clear = lambda : os.system('clear')
        clear()

# Imprime el menu principal
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

# Lee la opcion a elegir del menu principal
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

# Imprime la lista de jugadores entrenados
def printPlayers(players):
    print ("Jugadores actuales:")
    print("-> 0 - Jugador random sin entrenar")
    for p in players:
        print("-> ", end="")
        print(str(index), end="")
        print(" - ", end="")
        print("Jugador ", end="")
        print(p['name'])
        index = index + 1
    print ("")

# Imprime las opciones de tipo de jugador y lee la opcion elegida
def printPlayerType():
    print ("")
    print ("-> Elija un tipo de jugador para entrenar: ")
    print ("-> DEFAULT: 2")
    print ("1. VS Random")
    print ("2. VS Si Mismo")

    try:
        playerType = int( input() )

        if playerType < 1 or playerType > 2:
            return (PlayerType.TRAINED_SELF, "Si Mismo")
        else:
            if playerType == 1:
                playerType = PlayerType.TRAINED_RANDOM
                playerName = "Random"
            elif playerType == 2:
                playerType = PlayerType.TRAINED_SELF
                playerName = "Si Mismo"

        return (playerType, playerName)

    except:
        return (PlayerType.TRAINED_SELF, "Si Mismo")
    
# Imprime las opciones de cantidad de iteraciones y lee la opcion elegida
def printTrainingIterations():
    print ("")
    print ("-> Ingrese la cantidad de iteraciones (por defecto 100): ")
    print ("-> DEFAULT: 100")
    try:
        iters = int( input() )
        return iters
    except:
        return 100

# Imprime las opciones de ratio de aprendizaje y lee la opcion elegida
def printLearningRate():
    print ("")
    print ("-> Ingrese el ratio de aprendizaje (por defecto 0.5): ")
    try:
        learningRate = float( input() )
        if learningRate < 0 or learningRate > 1:
            return 0.5
        return learningRate
    except:
        return 0.5

# Imprime las opciones de pesos iniciales y lee la opcion elegida
def printInitialWeights():
    print ("")
    print ("-> Ingrese la lista de pesos iniciales (por defecto [0.9, 0.9, 0.9]): ")
    try:
        weights = input()
        weights = weights.split(',')
        weights = [float(w) for w in weights]
        return learningRate
    except:
        return [0.9, 0.9, 0.9]


### METODOS AUXILIARES - TABLERO
### ----------------------------

# Imprime una casilla, ya sea vacia o con una pieza
def printToken(slot):
    token = slot.getToken()
    print("(", end="")
    if token == GameTokens.EMPTY:
        print("       ", end="")
    elif token == GameTokens.PLAYER1:
        cprint("   O   ", 'yellow', end="")
    elif token == GameTokens.PLAYER2:
        cprint("   O   ", 'magenta', end="")
    print(")", end="")

# Imprime una casilla y sus coordenadas, ya sea vacia o con una pieza
def printSlot(slot):
    (x,y) = slot.getVPos()
    token = slot.getToken()
    print("(", end="")         
    if x > 0:
        cprint("+", 'red', end="")
        cprint(x, 'red', end=' ')
    elif x == 0:
        cprint("+", 'green', end="")
        cprint(x, 'green', end=' ')
    else:
        cprint(x, 'cyan', end=' ')

    if token == GameTokens.EMPTY:
        print("X", end=" ")
    elif token == GameTokens.PLAYER1:
        cprint("O", 'yellow', end=" ")
    elif token == GameTokens.PLAYER2:
        cprint("O", 'magenta', end=" ")

    if y > 0:
        cprint("+", 'red', end="")
        cprint(y, 'red', end='')
    elif y == 0:
        cprint("+", 'green', end="")
        cprint(y, 'green', end='')
    else:
        cprint(y, 'cyan', end='')
    print(")", end="")

# Imprime el tablero en forma de matriz
def printBoardMatrix(matrix, length):
    for y in range(0, length):
        for x in range(0, length):
            printSlot(matrix[x,y])

        print("")
        print("")

    print("")

# Imprime el tablero en forma de rombo
def printBoardHex(matrix, showGrid, fromVirtual):

    print("")

    limit = 1
    x = 4

    for y in range(-8, 1):
        
        for s in range(0, 9 - limit):
            print("    ", end="")

        for i in range(0, limit):
            xAux = x + i
            (x3,y3) = fromVirtual((xAux,y))
            
            if showGrid:
                printSlot(matrix[x3,y3])
            else:
                printToken(matrix[x3,y3])
        
        print("")
        print("")

        x = x - 1
        limit = limit + 1

    limit = 8
    x = -4

    for y in range(1, 9):

        for s in range(0, 9 - limit):
            print("    ", end="")

        for i in range(limit, 0, -1):
            xAux = x + limit - i
            (x3,y3) = fromVirtual((xAux,y))

            if showGrid:
                printSlot(matrix[x3,y3])
            else:
                printToken(matrix[x3,y3])
        
        print("")
        print("")

        limit = limit - 1

    print("")
