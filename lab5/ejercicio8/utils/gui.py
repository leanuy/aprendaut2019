### DEPENDENCIAS
### ------------------

import os
import sys
import re
from termcolor import colored, cprint

from .const import MenuOps, PlayerType, GameMode, GameTokens, ModelTypes, InputLayerTypes, ActivationFunctions, ArchiveOps, CompareOps

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
    print ("#        MENÚ - Laboratorio 5 (Damas Chinas)        #")
    print ("#                                                   #")
    print ("#####################################################")
    print ("")
    printPlayers(players)
    
    print ("General:")
    print ("1. Entrenar modelo")
    print ("2. Cargar modelo")
    print ("3. Guardar modelo")
    print ()

    print ("Evaluación:")
    print ("4. Evaluar modelo")
    print ("5. Buscar mejor modelo")
    print ("6. Comparar modelos")
    print ()

    print ("Simulación:")
    print ("7. Simular partida contra modelo")
    print ("8. Simular partida entre modelos")
    print ("9. Simular torneo")
    print ()

    print ("0. Salir")

# Lee la opcion a elegir del menu principal
def printMenuOption():
    print ("")   
    print ("-> Elija una opción: ")
    op = int( input() )

    if op < 1 or op > 9:
        sys.exit()
    else:
        if op == 1:
            op = MenuOps.TRAIN
        elif op == 2:
            op = MenuOps.LOAD
        elif op == 3:
            op = MenuOps.SAVE
        elif op == 4:
            op = MenuOps.EVALUATE
        elif op == 5:
            op = MenuOps.SEARCH
        elif op == 6:
            op = MenuOps.COMPARE
        elif op == 7:
            op = MenuOps.PLAY_VS_IA
        elif op == 8:
            op = MenuOps.WATCH_IA_VS_IA
        elif op == 9:
            op = MenuOps.TOURNEY

    return op

# Imprime la lista de jugadores entrenados
def printPlayers(players):
    print ("Jugadores actuales:")
    print("-> 0 - Jugador: Random sin entrenar")
    index = 1
    for player in players:
        print()
        print("-> ", end="")
        print(str(index), end="")
        print(" - ", end="")
        print("Modelo: ", end="")
        print(player['name'])

        print("--> Metadatos:")
        print("    Entrenado VS: ", end="")
        print(player['type'])
        print("    Tiempo de entrenamiento: ", end="")
        print(player['time'], end=" ")
        print("segundos")
        print("    Cantidad de iteraciones: ", end="")
        print(player['iterations'])
        print("    Cantidad máxima de turnos por juego: ", end="")
        print(player['maxRounds'])

        print("--> Parámetros:")

        if player['modelType'] == ModelTypes.NEURAL:
            print("    Representación del tablero: ", end="")
            print(player['inputLayer'])
            print("    Cantidad de capas ocultas: ", end="")
            print(player['hiddenLayer'])
            print("    Cantidad de neuronas por capa oculta: ", end="")
            print(player['hiddenNeuron'])
            print("    Función de activación: ", end="")
            print(player['activationFunction'])
        else:
            print("    Pesos iniciales: ", end="")
            print(player['initialWeights'])
            print("    Pesos finales: ", end="")
            print(player['finalWeights'])
        
        print("    Ratio de aprendizaje: ", end="")
        print(player['learningRate'])

        print("--> Resultados:")
        print("    Cantidad de partidas ganadas, perdidas, empatadas: ", end="")
        print(player['results'])
        print("    Porcentaje de partidas ganadas: ", end="")
        print(player['results'][0] / player['iterations'])

        index = index + 1
    print ("")

# Elegir un jugador de la lista de jugadores
def pickPlayer(players, message = "-> Elija un jugador por el índice: "):
    printClear()
    printPlayers(players)

    try:
        player = int(input(message))
        if player >= 0 and player < len(players) + 1:
            print("")
            return player
        else:
            # El índice ingresado no corresponde a ningún jugador!
            return pickPlayer(players, message)
    except:
        # El índice ingresado no corresponde a ningún jugador!
        return pickPlayer(players, message)
    
### METODOS AUXILIARES - ENTRENAMIENTO
### -------------------------

# Imprime las opciones de tipo de jugador y lee la opcion elegida
def printPlayerType(showdown = True):
    print ("")
    print ("-> Elija un tipo de jugador para entrenar: ")
    print ("-> DEFAULT: 2")
    print ("1. VS Random")
    print ("2. VS Si Mismo")
    if showdown:
        print ("3. VS otra IA (Training con retroalimentación mutua)")

    try:
        playerType = int( input() )

        if playerType < 1 or playerType > 3:
            return (PlayerType.TRAINED_SELF)
        elif playerType == 1:
            playerType = PlayerType.TRAINED_RANDOM
        elif playerType == 2:
            playerType = PlayerType.TRAINED_SELF
        elif playerType == 3:
            playerType = PlayerType.TRAINED_SHOWDOWN
            
        return playerType

    except:
        return PlayerType.TRAINED_SELF

# Lee el tipo de modelo a usar
def printModelOptions():
    print ("")   
    print ("-> Decida el tipo de modelo: ")
    print ("-> DEFAULT: 2")
    print ("1. Función lineal (lab 1)")
    print ("2. Red neuronal (lab 5)")

    try:
        model = int( input() )
        if model < 1 or model > 2:
            return (ModelTypes.NEURAL, getModelName(ModelTypes.NEURAL))
        else:
            if model == 1:
                model = ModelTypes.LINEAR
            elif model == 2:
                model = ModelTypes.NEURAL
            return (model, getModelName(model))
    except:
        return (ModelTypes.NEURAL, getModelName(ModelTypes.NEURAL))

# Lee la representación del tablero a usar para la red neuronal
def printInputLayer():
    print ("")   
    print ("-> Decida cantidad de neuronas en capa de entrada (representación del tablero): ")
    print ("-> DEFAULT: 1")
    print ("1. Métricas (8)")
    print ("2. Celdas (81)")

    try:
        rep = int( input() )
        if rep < 1 or rep > 2:
            return InputLayerTypes.METRICS
        else:
            if rep == 1:
                rep = InputLayerTypes.METRICS
            elif rep == 2:
                rep = InputLayerTypes.BOARD
            return rep
    except:
        return InputLayerTypes.METRICS

#  Lee la cantidad de capas ocultas para la red neuronal
def printHiddenLayers():
    print ("")
    print ("-> Decida cantidad de capas ocultas: ")
    print ("-> DEFAULT: 1")
    try:
        layers = int( input() )
        return layers
    except:
        return 1

#  Lee la cantidad de neuronas en cada capa oculta para la red neuronal
def printHiddenNeurons():
    print ("")
    print ("-> Decida cantidad de neuronas por capa oculta: ")
    print ("-> DEFAULT: 10")
    try:
        neurons = int( input() )
        return neurons
    except:
        return 10

# Lee que tipo de función de activación utilizar
def printActivationFunction():
    print ("")   
    print ("-> Decida el tipo de función de activación a utilizar: ")
    print ("-> DEFAULT: 1")
    print ("1. Rectificador (ReLU)")
    print ("2. Logística (Sigmoide)")
    print ("3. Tangente hiperbólica (Tanh)")

    try:
        func = int( input() )
        if func < 1 or func > 3:
            return ActivationFunctions.RELU
        else:
            if func == 1:
                func = ActivationFunctions.RELU
            elif func == 2:
                func = ActivationFunctions.SIGMOID
            elif func == 3:
                func = ActivationFunctions.TANH
            return func
    except:
        return ActivationFunctions.RELU

# Imprime las opciones de ratio de aprendizaje y lee la opcion elegida
def printLearningRateNeural():
    print ("")
    print ("-> Ingrese el tipo de ratio de aprendizaje y su valor inicial: ")
    print ("-> Posibles tipos: 'constant' o 'invscaling'")
    print ("-> Posibles valores: [0..1]")
    print ("-> DEFAULT: 'constant', 0.001")

    try:
        learningRate = input()
        learningRateType, learningRateValue = learningRate.split(',')
        return (learningRateType, float(learningRateValue))
    except:
        return ('constant', 0.001)

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
    print ("-> DEFAULT: 300")
    try:
        rounds = int( input() )
        return rounds
    except:
        return 300

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
    print ("-> Ingrese la lista de pesos iniciales: [w0, wA1, wA2, wB1, wB2, wC1, wC2, wD1, wD2]")
    print ("-> DEFAULT: [0.1, -0.9, 0.9, -0.1, 0.1, 0.1, -0.1, -0.1, 0.1]")
    try:
        weights = input()
        weights = weights.split(',')
        weights = [float(w) for w in weights]
        if len(weights != 9):
            return [0.1, -0.9, 0.9, -0.1, 0.1, 0.1, -0.1, -0.1, 0.1]
        return weights
    except:
        return [0.1, -0.9, 0.9, -0.1, 0.1, 0.1, -0.1, -0.1, 0.1]

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

# Pregunta al usuario si desea espectar un duelo
def printSpectateOptions():
    print ("")
    print ("-> Desea espectar las partidas? (y/n) ")
    print ("-> DEFAULT: n")
    spectate = input()
    if spectate == 'y':
        return True
    else:
        return False

# Imprime los datos de entrenamiento de un jugador
def printTrainedPlayer(player, index = 0):

    print("-> ", end="")
    if index != 0:
        print(str(index), end="")
        print(" - ", end="")
    print("Modelo: ", end="")
    print(player['name'])

    print("--> Metadatos:")
    print("    Entrenado VS: ", end="")
    print(player['type'])
    print("    Tiempo de entrenamiento: ", end="")
    print(player['time'], end=" ")
    print("segundos")
    print("    Cantidad de iteraciones: ", end="")
    print(player['iterations'])
    print("    Cantidad máxima de turnos por juego: ", end="")
    print(player['maxRounds'])

    print("--> Parámetros:")

    if player['modelType'] == ModelTypes.NEURAL:
        print("    Representación del tablero: ", end="")
        print(player['inputLayer'])
        print("    Cantidad de capas ocultas: ", end="")
        print(player['hiddenLayer'])
        print("    Cantidad de neuronas por capa oculta: ", end="")
        print(player['hiddenNeuron'])
        print("    Función de activación: ", end="")
        print(player['activationFunction'])
    else:
        print("    Pesos iniciales: ", end="")
        print(player['initialWeights'])
        print("    Pesos finales: ", end="")
        print(player['finalWeights'])
    
    print("    Ratio de aprendizaje: ", end="")
    print(player['learningRate'])

    print("--> Resultados:")
    print("    Cantidad de partidas ganadas, perdidas, empatadas: ", end="")
    print(player['results'])
    print("    Porcentaje de partidas ganadas: ", end="")
    print(player['results'][0] / player['iterations'])

    print()

def getModelName(modelType):
    if modelType == ModelTypes.LINEAR:
        return "Función Lineal"
    elif modelType == ModelTypes.NEURAL:
        return "Red Neuronal"
    return ""

### METODOS AUXILIARES - MANEJO
### ---------------------------

# Lee el tipo de carga/guardado
def printArchiveOptions(op):
    print ("")
    if op == ArchiveOps.LOAD:
        print ("-> Decida el tipo de carga que desea hacer: ")
        print ("-> DEFAULT: 1")
        print ("1. Carga única")
        print ("2. Carga masiva")

        try:
            load = int( input() )
            if load < 1 or load > 2:
                return ArchiveOps.SINGLE
            else:
                if load == 1:
                    load = ArchiveOps.SINGLE
                elif load == 2:
                    load = ArchiveOps.MASSIVE
                return load
        except:
            return ArchiveOps.SINGLE
    else:
        print ("-> Decida el tipo de guardado que desea hacer: ")
        print ("-> DEFAULT: 1")
        print ("1. Guardado único")
        print ("2. Guardado masivo")

        try:
            load = int( input() )
            if load < 1 or load > 2:
                return ArchiveOps.SINGLE
            else:
                if load == 1:
                    load = ArchiveOps.SINGLE
                elif load == 2:
                    load = ArchiveOps.MASSIVE
                return load
        except:
            return ArchiveOps.SINGLE

def printSavePlayer():
    print("")
    print("-> Ingrese el nombre del archivo en donde guardar al jugador (No ingrese nada para no guardarlo)")
    return input()

def printLoadPlayer():
    print("")
    print("-> Ingrese el nombre del archivo que contiene al jugador")
    return input()

def printLoadMassive():
    print ("")
    print ("-> Ingrese el prefijo de jugadores que desea cargar")
    print ("-> DEFAULT: - (Ingresar nada)")
    print ("--> No ingrese nada para cargar todos")
    print ("--> Ingrese restricciones en base a los nombres de archivo (self o random, board o metrics, constant o invscaling, etc.)")
    print ("--> Ingrese múltiples restricciones en el orden correspondiente (oponente_representacion_capasocultas_neuronasocultas_activacion_ratio) ")
    return input()

### METODOS AUXILIARES - COMPARACIÓN
### ---------------------------

def printCompareOption():
    print ("")   
    print ("-> Elija una opción para comparar: ")
    print ("-> DEFAULT: 1")
    print ("1. Comparar ratio de partidas ganadas")
    print ("2. Comparar ratio de victorias")
    print ("3. Comparar ratio de partidas ganadas en función de capas ocultas")
    print ("4. Comparar ratio de partidas ganadas en función de neuronas ocultas")
    print ("5. Comparar ratio de partidas ganadas en función de activación")
    print ("6. Comparar ratio de partidas ganadas en función de ratio de aprendizaje")    
    
    try:
        op = int( input() )
        if op < 1 or op > 6:
            return CompareOps.WIN_RATE
        else:
            if op == 1:
                op = CompareOps.WIN_RATE
            elif op == 2:
                op = CompareOps.VICTORY_RATE
            elif op == 3:
                op = CompareOps.HIDDEN_LAYERS
            elif op == 4:
                op = CompareOps.HIDDEN_NEURONS
            elif op == 5:
                op = CompareOps.ACTIVATION
            elif op == 6:
                op = CompareOps.LEARNING_RATE
            return op
    except:
        return CompareOps.WIN_RATE

### METODOS AUXILIARES - PARTIDA
### ---------------------------

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

# Imprime los features ingresados
def printFeatures(features):
    print("Suma cuadrada de distancia al extremo: " + str(features[1])) + ', ' + str(features[2])
    print("Suma cuadrada de distancia al centro: " + str(features[3])) + ', ' + str(features[4])
    print("Suma de maxima cantidad de saltos: " + str(features[5])) + ', ' + str(features[6])
    print("Suma cuadrada de distancia al hex del goal vacio mas cercano: " + str(features[7])) + ', ' + str(features[8])
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
