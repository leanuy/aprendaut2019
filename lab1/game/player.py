### DEPENDENCIAS
### ------------------

import random

from utils.const import PlayerType

### CLASE PRINCIPAL
### ------------------

class Player():

    ### METODOS AUXILIARES
    ### -------------------


    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, playerNumber, playerType):
        
        self.playerNumber = playerNumber
        self.playerType = playerType

    ### METODOS PRINCIPALES
    ### -------------------

    # 
    def chooseMove(self, board):
        
        playerTokens = board.getPlayerSlots(self.playerNumber)
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

            #print("Ficha elegida: " + str((fromVX, fromVY)))

            # Marcarla como usada para no volver a elegirla si no llega a ser
            # posible moverla
            usedTokens[tokenIndex] = True

            # Obtener la lista de posibles movimientos desde FROM y si existe alguno
            # elegir aleatoriamente entre ellos y devolverlo
            moves = board.getPossibleMoves(self.playerNumber, fromVX, fromVY)
            #print("Posibles movimientos: " + str(moves))
            #print()
            #input()
            if moves:
                return ((fromVX, fromVY), random.choice(moves))

        return ((0,0),(0,0))