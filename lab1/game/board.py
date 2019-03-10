### DEPENDENCIAS
### ------------------

import numpy as np

from utils.const import GameMode, GameTokens, GameTokenMoves

### CLASE AUXILIAR
### ------------------

class Slot():

    ### CONSTRUCTOR
    ### -------------------

    def __init__(self, rPos, vPos, token):
        
        self.rPos = rPos
        self.vPos = vPos
        self.token = token

    ### GETTERS y SETTERS
    ### -------------------

    def getRPos(self):
        return self.rPos
    def setRPos(self, rPos):
        self.rPos = rPos

    def getVPos(self):
        return self.vPos
    def setVPos(self, vPos):
        self.vPos = vPos

    def getToken(self):
        return self.token
    def setToken(self, token):
        self.token = token

    def isEmpty(self):
        return self.token == GameTokens.EMPTY


### CLASE PRINCIPAL
### ------------------

class Board():

    ### METODOS AUXILIARES
    ### -------------------

    # Restricción 1 y su inversa al momento de parsear el tablero virtual al real
    def restriction1(self, x, y):
        return (x - self.radius, - y + self.radius)
    def inverse1(self, x, y):
        return (x + self.radius, - y + self.radius)

    # Restricción 2 y su inversa al momento de parsear el tablero virtual al real
    def restriction2(self, x, y):
        if x + y > self.radius:
            return (x, y - self.length)
        elif x + y < -self.radius:
            return (x, y + self.length)
        return (x, y)
    def inverse2(self, x, y):
        if y > self.radius:
            return (x, y - self.length)
        elif y < -self.radius:
            return (x, y + self.length)
        return (x, y)

    # Parseo de coordenadas reales a virtuales y viceversa
    def toVirtual(self, pair):
        (x, y) = pair
        (x2, y2) = self.restriction1(x, y)
        return self.restriction2(x2, y2)
    def fromVirtual(self, pair):
        (x, y) = pair
        (x2, y2) = self.inverse2(x, y)
        return self.inverse1(x2, y2)

    # Comprueba que las coordenadas virtuales existan
    def isInVirtualBounds(self, pair):
        return pair in self.slots

    # Rellena el tablero con las fichas correspondientes
    def fillPlayers(self, x, y):
        if x + y > self.radius:
            return GameTokens.PLAYER1
        elif x + y < -self.radius:
            return GameTokens.PLAYER2
        return GameTokens.EMPTY


    ### CONSTRUCTOR
    ### -------------------

    def __init__(self):
        
        self.radius = 4
        self.length = 9
        self.matrix = np.zeros((self.length, self.length), dtype=object)
        self.slots = []

        for y in range(0, self.length):
            for x in range(0, self.length):
                self.matrix[x,y] = Slot((x,y), self.restriction1(x,y), 0)
                
        for y in range(0, self.length):
            for x in range(0, self.length):
                (x2, y2) = self.matrix[x,y].getVPos()
                self.matrix[x,y].setVPos(self.restriction2(x2,y2))
                self.matrix[x,y].setToken(self.fillPlayers(x2,y2))
                self.slots.append(self.matrix[x,y].getVPos())

    ### GETTERS y SETTERS
    ### -------------------

    def getMatrix(self):
        return self.matrix

    def getRadius(self):
        return self.radius
    
    def getLength(self):
        return self.length

    ### METODOS PRINCIPALES
    ### -------------------

    # 
    def getPlayerSlots(self, player):
        slots = []
        for x in range(0, self.length):
            for y in range(0, self.length):
                if self.matrix[x,y].getToken() == player:
                    slots.append(self.matrix[x,y].getVPos())
        return slots

    # Dado un par de coordenadas virtuales genera una lista de posibles movimientos
    # para la pieza en las coordenadas dadas, teniendo en cuenta su jugador
    def getPossibleMoves(self, player, vX, vY):
        moves = []

        northwest = (vX, vY-1)
        west = (vX-1, vY)
        southwest = (vX-1, vY+1)
        southeast = (vX, vY+1)
        east = (vX+1, vY)
        northeast = (vX+1, vY-1)

        rNorthwest = self.fromVirtual(northwest)
        rWest = self.fromVirtual(west)
        rSouthwest = self.fromVirtual(southwest)
        rSoutheast = self.fromVirtual(southeast)
        rEast = self.fromVirtual(east)
        rNortheast = self.fromVirtual(northeast)

        if self.isInVirtualBounds(northwest) and self.matrix[rNorthwest].isEmpty():
            moves.append(northwest)
        if self.isInVirtualBounds(west) and self.matrix[rWest].isEmpty():
            moves.append(west)
        if self.isInVirtualBounds(southwest) and self.matrix[rSouthwest].isEmpty():
            moves.append(southwest)
        if self.isInVirtualBounds(southeast) and self.matrix[rSoutheast].isEmpty():
            moves.append(southeast)
        if self.isInVirtualBounds(east) and self.matrix[rEast].isEmpty():
            moves.append(east)
        if self.isInVirtualBounds(northeast) and self.matrix[rNortheast].isEmpty():
            moves.append(northeast)

        return moves

    # Dado un jugador y un movimiento de un par de coordenadas virtuales a otro
    # comprueba si es posible y lo hace en caso de serlo, o devuelve el error correspondiente
    def moveToken(self, player, fromVX, fromVY, toVX, toVY):
        
        # Obtener las coordenadas en la matriz para FROM
        (fromRX, fromRY) = self.fromVirtual((fromVX, fromVY))

        # Comprobar si las coordenadas FROM son validas
        if not self.isInVirtualBounds((fromVX, fromVY)):
            return GameTokenMoves.INVALID_COORDS

        # Comprobar si en FROM hay una ficha del jugador PLAYER
        if self.matrix[fromRX,fromRY].getToken() != player:
            return GameTokenMoves.TOKEN_FROM

        # Obtener las coordenadas en la matriz para TO
        (toRX, toRY) = self.fromVirtual((toVX, toVY))

        # Comprobar si las coordenadas TO son validas
        if not self.isInVirtualBounds((toVX, toVY)):
            return GameTokenMoves.INVALID_COORDS

        # Comprobar si en TO hay una ficha o esta vacío
        if not self.matrix[toRX,toRY].isEmpty():
            return GameTokenMoves.TOKEN_TO
        
        # Comprobar si es posible moverse de FROM a TO
        isPossible = False
        moves = self.getPossibleMoves(player, fromVX, fromVY)
        for x in moves:
            if x == (toVX, toVY):
                isPossible = True
        if not isPossible:
            return GameTokenMoves.INVALID_MOVE

        # Realizar el movimiento
        self.matrix[fromRX,fromRY].setToken(GameTokens.EMPTY)
        self.matrix[toRX,toRY].setToken(player)

        return GameTokenMoves.VALID_MOVE
