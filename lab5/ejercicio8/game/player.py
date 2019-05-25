### DEPENDENCIAS
### ------------------

import random

from model.model_concept import ModelConcept
from random import randint

from utils.const import PlayerType

### CLASE PRINCIPAL
### ------------------

class Player():

    ### METODOS AUXILIARES
    ### -------------------


    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, playerNumber, playerType, model = None):
        
        # Numero de las fichas del jugador en la partida
        self.playerNumber = playerNumber
        
        # Tipo de jugador
        # 1. Entrenado contra un random
        # 2. Entrenado contra si mismo
        # 0. Random
        self.playerType = playerType

        # Modelo del jugador entrenado. Si es un jugador random,
        # es None y no se usa
        self.model = model

        # Último movimiento para no hacer loops
        self.historialFrom = []
        self.historialTo = []

    ### GETTERS y SETTERS
    ### -------------------

    def getModel(self):
        return self.model
    def setModel(self, m):
        self.model = m

    def getPlayerType(self):
        return self.playerType
    
    def setPlayerNumber(self, n):
        self.playerNumber = n

    ### METODOS PRINCIPALES
    ### -------------------

    # Dado un tablero elige el un movimiento
    # -> Si es un jugador random lo elige aleatoriamente
    # -> Si es un jugador entrenado, evalua todas las posibilidades con el modelo
    # y elige la mejor evaluada
    def chooseMove(self, board):
        
        # Obtener las fichas del jugador
        playerTokens = board.getPlayerSlots(self.playerNumber)

        if self.playerType == PlayerType.RANDOM:

            # Lista auxiliar para no repetir fichas ya elegidas aleatoriamente
            usedTokens = [False for token in playerTokens]

            # Comprobar si se agotaron todos los posibles movimientos. En ese caso
            # se retorna (0,0) a (0,0) y el juego interpreta que no hay movimientos
            while not all(token for token in usedTokens):

                # Obtener ficha aleatoria que no haya sido checkeada
                (fromVX, fromVY) = random.choice(playerTokens)
                tokenIndex = playerTokens.index((fromVX, fromVY))
                while usedTokens[tokenIndex]:
                    (fromVX, fromVY) = random.choice(playerTokens)
                    tokenIndex = playerTokens.index((fromVX, fromVY))

                # Marcarla como usada para no volver a elegirla si no llega a ser
                # posible moverla
                usedTokens[tokenIndex] = True

                # Obtener la lista de posibles movimientos desde FROM y si existe alguno
                # elegir aleatoriamente entre ellos y devolverlo
                (movesForward, movesBackward) = board.getPossibleMoves(self.playerNumber, fromVX, fromVY)

                # Preferimos movimientos hacia adelante siempre que estos sean posibles
                if movesForward:
                    moves = movesForward
                else:
                    moves = movesBackward

                if moves:
                    return ((fromVX, fromVY), random.choice(moves))

            return ((0,0),(0,0))

        else:

            bestFrom = None
            bestTo = None
            bestEvaluation = 0
            allMovesForward = []
            allMovesBackward = []

            # Se recorre todas las piezas del jugador
            for token in playerTokens:
                
                # Se obtiene la lista de posibles movimientos desde FROM
                (fromVX, fromVY) = token
                (movesForward, movesBackward) = board.getPossibleMoves(self.playerNumber, fromVX, fromVY)

                for movef in movesForward:
                    allMovesForward.append((token, movef))
                for moveb in movesBackward:
                    allMovesBackward.append((token, moveb))

            # Preferimos movimientos hacia adelante siempre que estos sean posibles
            if allMovesForward:
                moves = allMovesForward
            else:
                moves = allMovesBackward

            # Se recorre todos los posibles movimientos, evaluando el tablero tras cada uno
            for (fromVX, fromVY), (toVX, toVY) in moves:
                # No permitimos movimientos inversos a los últimos 3
                if (self.historialFrom) and ((toVX,toVY) in self.historialFrom[-3:]):
                    continue

                board.moveToken(self.playerNumber, fromVX, fromVY, toVX, toVY)
                features = board.getFeatures(self.playerNumber, self.model.options['modelType'])
                evaluation = self.model.evaluate(features)

                # Si es el primer movimiento evaluado o tiene la mejor evaluacion conseguida
                # hasta ahora, se guarda como el mejor movimiento
                if bestTo == None or evaluation >= bestEvaluation:
                    if bestTo == None or evaluation > bestEvaluation:
                        best_moves = []
                    bestFrom = (fromVX, fromVY)
                    bestTo = (toVX, toVY)
                    bestEvaluation = evaluation
                    best_moves.append((bestFrom, bestTo))
                # Se deja el tablero en el estado anterior
                board.undoToken(self.playerNumber, fromVX, fromVY, toVX, toVY)

            try:
                move = best_moves[randint(0,len(best_moves)-1)]
            except:
                # HACK: A veces pasa que todos los movimientos posibles son inversos a movimientos ya hechos
                # (por lo general con otra pieza). Entonces elegimos un movimiento aleatorio
                move = moves[randint(0,len(moves)-1)]
            ((fromX, fromY), (toX, toY)) = move
            self.historialFrom.append((fromX,fromY))
            self.historialTo.append((toX, toY))
            return move