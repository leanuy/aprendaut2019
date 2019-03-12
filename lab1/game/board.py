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
        
        # Posición real (x,y) en el tablero matriz
        self.rPos = rPos

        # Posición virtual (x,y) en el tablero hexagonal
        self.vPos = vPos

        # Pieza del slot (jugador1, jugador2 o vacio)
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
        
        # Radio del hexagono
        self.radius = 4
        
        # Largo de extremo a extremo
        self.length = 9
        
        # Representación del tablero hexagonal en matriz cuadrada
        self.matrix = np.zeros((self.length, self.length), dtype=object)
        
        # Lista con todas las posibles coordenadas virtuales (para comprobar validez)
        self.slots = []

        # Utils
        # Versores con direcciones de desplazamiento
        self.axial_directions = {
            'northwest': (0,-1),
            'west': (-1,0),
            'southwest': (-1,1),
            'southeast': (0,1),
            'east': (1,0),
            'northeast': (1,-1)
        }

        # Rellenado del tablero
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

    # Devuelve una lista con las coordenadas virtuales de las piezas del jugador
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
        
        (moves, jumps) = self.getPossibleAdjacentMoves(player, (vX, vY))

        visitedJumps = []
        for jump in jumps:
            moves.extend(self.getPossibleJumpMoves(player, (vX, vY), jump, visitedJumps))

        return moves

    # Dado un par de coordenadas virtuales genera un par compuesto por unalista 
    # de posibles movimientos a casillas adyacentes o de posibles casillas a saltar
    def getPossibleAdjacentMoves(self, player, position):
        moves = []
        jumps = []

        (vX, vY) = position

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

        if self.isInVirtualBounds(northwest): 
            if self.matrix[rNorthwest].isEmpty():
                moves.append(northwest)
            else:
                jumps.append(northwest)

        if self.isInVirtualBounds(west):
            if self.matrix[rWest].isEmpty():
                moves.append(west)
            else:
                jumps.append(west)

        if self.isInVirtualBounds(southwest):
            if self.matrix[rSouthwest].isEmpty():
                moves.append(southwest)
            else:
                jumps.append(southwest)

        if self.isInVirtualBounds(southeast):
            if self.matrix[rSoutheast].isEmpty():
                moves.append(southeast)
            else:
                jumps.append(southeast)

        if self.isInVirtualBounds(east):
            if self.matrix[rEast].isEmpty():
                moves.append(east)
            else:
                jumps.append(east)

        if self.isInVirtualBounds(northeast):
            if self.matrix[rNortheast].isEmpty():
                moves.append(northeast)
            else:
                jumps.append(northeast)

        return (moves, jumps)

    # Dado un par de coordenadas virtuales y un vecino a saltar, genera una lista
    # de posibles saltos para la pieza en las coordenadas dadas
    def getPossibleJumpMoves(self, player, fromJump, jump, visitedJumps):

        moves = []

        if not (fromJump, jump) in visitedJumps:

            visitedJumps.append((fromJump, jump))
            
            (fromVX, fromVY) = fromJump
            (vX, vY) = jump
            
            (relX, relY) = ((fromVX - vX) * -1, (fromVY - vY) * -1)
            possibleJump = (vX + relX, vY + relY)
            rPossibleJump = self.fromVirtual(possibleJump)

            if self.isInVirtualBounds(possibleJump) and self.matrix[rPossibleJump].isEmpty():
                moves.append(possibleJump)

                (adjacentMoves, adjacentJumps) = self.getPossibleAdjacentMoves(player, possibleJump)
                for aJump in adjacentJumps:
                    if aJump != jump:
                        moves.extend(self.getPossibleJumpMoves(player, possibleJump, aJump, visitedJumps))

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

    # Dado un jugador y un movimiento ya realizado, devuelve el tablero al estado en el que
    # se encontraba antes de realizar el movimiento
    # DETALLE: Este metodo debe ser usado solamente luego de moveToken en un entrenamiento
    def undoToken(self, player, fromVX, fromVY, toVX, toVY):
        
        # Obtener las coordenadas en la matriz para FROM y TO
        (fromRX, fromRY) = self.fromVirtual((fromVX, fromVY))
        (toRX, toRY) = self.fromVirtual((toVX, toVY))

        # Deshacer el movimiento
        self.matrix[fromRX,fromRY].setToken(player)
        self.matrix[toRX,toRY].setToken(GameTokens.EMPTY)

    # Checkea si el jugador 'player' ganó en el tablero actual 
    def checkWin(self, player):
        playerSlots = self.getPlayerSlots(player)
        if player == GameTokens.PLAYER1:
            for slot in playerSlots:
                (x, y) = slot
                if y <= self.radius:
                    return False
        else:
            for slot in playerSlots:
                (x, y) = slot
                if y >= -self.radius:
                    return False

        return True

    # Obtiene los coeficientes de la representacion actual del tablero
        # Penalizar A: Cuanto mas lejos estas de la esquina opuesta en comparacion a tu contricante, peor estas
        # Penalizar B: Cuanto mas lejos estas de la linea en comparacion a tu contricante, peor estas
        # Bonificar C: Cuanto mayor es el posible avance vertical, mejor estas
    def getFeatures(self, player):
        (A1, B1, C1) = self.get_features_for_player(GameTokens.PLAYER1)
        (A2, B2, C2) = self.get_features_for_player(GameTokens.PLAYER2)
        return [A2 - A1, B2 - B1, C1 - C2] if player == GameTokens.PLAYER1 else [A1 - A2, B1 - B2, C2 - C1]

    ### METODOS AUXILIARES
    ### -------------------

    def get_features_for_player(self, player):
        player_slots = self.getPlayerSlots(player)
        goal = (self.getRadius(), -(self.getLength()-1)) if player == GameTokens.PLAYER1 else (-self.getRadius(), self.getLength()-1)
        total_squared_distance_to_goal = 0
        total_squared_distance_to_center = 0
        sum_of_maximum_hop_to_goal = 0
        for slot in player_slots:
            # Ai = Suma cuadrada de la distancia a la esquina opuesta para todas las fichas del jugador i 
            total_squared_distance_to_goal += self.hex_distance(slot, goal)^2
            # Bi = Suma cuadrada de la distancia a la linea central para todas las fichas del jugador i 
            total_squared_distance_to_center += self.distance_to_vertical_center(slot)^2
            # Ci = Suma del maximo avance vertical posible para todas las fichas del jugador i
            sum_of_maximum_hop_to_goal += self.maximum_hop_to_goal_for_player(slot, player, goal)
        return [total_squared_distance_to_goal, total_squared_distance_to_center, sum_of_maximum_hop_to_goal]
    
    # Obtener distancia de una hex a otra
    # https://www.redblobgames.com/grids/hexagons/#distances
    def hex_distance(self, from_hex, to_hex):
        (fromX, fromY) = from_hex
        (toX, toY) = to_hex
        return max(abs(fromX - toX), abs(fromX + fromY - toX - toY), abs(fromY - toY))

    def distance_to_vertical_center(self, from_hex):
        (fromX, fromY) = from_hex
        centerY = fromY
        if centerY % 2 == 0: # Is even
            # Checks distance with the hex in the middle
            centerX = -centerY/2
            return self.hex_distance(from_hex, (centerX, centerY))
        else: # Is odd
            # There is no middle hex, so checks with the one on the northwest and northeast.
            # TODO: Esto se podria pulir si hay una forma facil de determinar si un hex esta al este u oeste de la vertical.
            west_centerX = -np.sign(centerY)*((abs(centerY) - 1)/2)
            east_centerX = -np.sign(centerY)*((abs(centerY) + 1)/2)
            return min(self.hex_distance(from_hex, (west_centerX, centerY)), self.hex_distance(from_hex, (east_centerX, centerY)))
    
    def maximum_hop_to_goal_for_player(self, from_hex, player, goal):
        (fromX, fromY) = from_hex
        moves = self.getPossibleMoves(player, fromX, fromY)
        maximum_hop = 0
        for move in moves:
            distance = self.hex_distance(move, goal)
            if distance > maximum_hop:
                maximum_hop = distance
        return maximum_hop

    # Mueve una celda en una dirección "east", "northwest", etc
    def hex_neighbor(self, hex, direction):
        (dirX, dirY) = self.axial_directions[direction]
        (hexX, hexY) = hex.getVPos()
        return (hexX + dirX, hexY + dirY)