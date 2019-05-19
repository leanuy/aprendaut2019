### DEPENDENCIAS
### ------------------

import os
import sys
import re
from termcolor import colored, cprint

from .const import MenuOps, PlayerType, GameMode, GameTokens, ModelTypes

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

# Lee la opcion a elegir del menu principal
def printModelOptions():
    print ("")   
    print ("-> Decida el tipo de modelo: ")
    print ("1. Aprendizaje conceptual (lab1)")
    print ("2. Q-Training profundo: Board")
    print ("3. Q-Training profundo: Metricas")
    model = int( input() )

    if model < 1 or model > 3:
        sys.exit()
    else:
        if model == 1:
            model = ModelTypes.CONCEPT
        elif model == 2:
            model = ModelTypes.NEURAL_BOARD
        elif model == 3:
            model = ModelTypes.NEURAL_METRICS
    return model

# Imprime la lista de jugadores entrenados
def printPlayers(players):
    print ("Jugadores actuales:")
    print("-> 0 - Jugador random sin entrenar")
    index = 1
    for p in players:
        print("-> ", end="")
        print(str(index), end="")
        print(" - ", end="")
        print("Jugador ", end="")
        print(p['name'])
        index = index + 1
    print ("")

# Lee la opcion a elegir del menu del juego
def printGameMenuOption():
    print("-> Ingrese su jugada o el numero de la opción deseada: ")
    print("---> Para mover la ficha (x,y) a la posicion (w,z) ingrese x,y w,z")
    print("---> Para ver las features de la ficha (x,y) ingrese x,y")
    print("---> Para pasar el turno ingrese PASS")
    print("---> 1 - Ver tablero normal")
    print("---> 2 - Ver tablero grilla")
    print("---> 3 - Ver tablero matriz")
    print("---> 4 - Ver tablero y features")
    print("---> 5 - Ver tablero y mis features")
    print("---> 0 - Abandonar")
    keyboard = input()
    keyboardToken = re.search(r"^[-+]?\d+,[-+]?\d+$", keyboard)
    return (keyboard, keyboardToken)

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
    print ("-> Ingrese la cantidad de iteraciones: ")
    print ("-> DEFAULT: 100")
    try:
        iters = int( input() )
        return iters
    except:
        return 100

# Imprime las opciones de cantidad de turnos y lee la opcion elegida
def printMaxRounds():
    print ("")
    print ("-> Ingrese la cantidad de turnos antes de declarar empate: ")
    print ("-> DEFAULT: 100")
    try:
        rounds = int( input() )
        return rounds
    except:
        return 100

# Imprime las opciones de ratio de aprendizaje y lee la opcion elegida
def printLearningRate():
    print ("")
    print ("-> Ingrese el ratio de aprendizaje: ")
    print ("-> DEFAULT: 0.5, 'var' para variable")
    learningRate = input()
    if learningRate == "var":
        return 'var'
    else:
        try:
            learningRate = float( learningRate )
            if learningRate < 0 or learningRate > 1:
                return 0.5
            return learningRate
        except:
            return 0.5

# Imprime las opciones de pesos iniciales y lee la opcion elegida
def printInitialWeights():
    print ("")
    print ("-> Ingrese la lista de pesos iniciales: [w0, wA, wB, wC, wD]")
    print ("-> DEFAULT: [0.9, 0.9, 0.9, 0.9, 0.9]")
    try:
        weights = input()
        weights = weights.split(',')
        weights = [float(w) for w in weights]
        return weights
    except:
        return [0.9, 0.9, 0.9, 0.9, 0.9]

# Pregunta al usuario si desea normalizar el modelo
def printNormalizeWeights():
    print ("")
    print ("-> Desea normalizar el los pesos? (y/n) ")
    print ("-> DEFAULT: n")
    normalized_model = input()
    if normalized_model == 'y':
        return True
    else:
        return False

# Pregunta al usuario si desea contar los empates
def printSkipOnDraw():
    print ("")
    print ("-> Desea contar una iteracion que empate? (y/n) ")
    print ("-> DEFAULT: n")
    notDraw = input()
    if notDraw == 'y':
        return True
    else:
        return False

# Imprime los datos de entrenamiento de un jugador
def printTrainedPlayer(player):

    print("-> Jugador Entrenado VS ", end="")
    print(player['name'])

    print("--> Tiempo de entrenamiento: ", end="")
    print(player['time'], end=" ")
    print("segundos")

    print("--> Cantidad de iteraciones: ", end="")
    print(player['iterations'])

    print("--> Cantidad máxima de turnos por juego: ", end="")
    print(player['maxRounds'])

    print("--> Ratio de aprendizaje: ", end="")
    print(player['learningRate'])

    print("--> Pesos iniciales: ", end="")
    print(player['initialWeights'])

    print("--> Pesos finales: ", end="")
    print(player['finalWeights'])

    print("--> Cantidad de partidas ganadas, perdidas, empatadas: ", end="")
    print(player['results'])

    print("--> Porcentaje de partidas ganadas: ", end="")
    print(player['results'][0] / player['iterations'])

    print()

# Imprime los features ingresados
def printFeatures(features):
    print("Suma cuadrada de distancia al extremo: " + str(features[0]))
    print("Suma cuadrada de distancia al centro: " + str(features[1]))
    print("Suma de maxima cantidad de saltos: " + str(features[2]))
    print("Suma cuadrada de distancia al hex del goal vacio mas cercano: " + str(features[3]))
    print()

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
