### DEPENDENCIAS
### ------------------

import numpy as np

from utils.const import GameMode

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


### CLASE PRINCIPAL
### ------------------

class Board():

    ### METODOS AUXILIARES
    ### -------------------

    def restriction1(self, x, y):
        return (x - 4, - y + 4)

    def inverse1(self, x, y):
        return (x + 4, -y + 4)

    def restriction2(self, x, y):
        if x + y > 4:
            return (x, y - 9)
        elif x + y < -4:
            return (x, y + 9)
        return (x, y)

    def inverse2(self, x, y):
        if y > 4:
            return (x, y - 9)
        elif y < -4:
            return (x, y + 9)
        return (x, y)

    # Rellena el tablero con las fichas correspondientes
    def fillPlayers(self, x, y):
        if x + y > 4:
            return 1
        elif x + y < -4:
            return 2
        return 0


    ### CONSTRUCTOR
    ### -------------------

    def __init__(self):
        
        self.radius = 4
        self.length = 9
        self.matrix = np.zeros((self.length, self.length), dtype=object)

        for y in range(0, self.length):
            for x in range(0, self.length):
                self.matrix[x,y] = Slot((x,y), self.restriction1(x,y), 0)
                
        for y in range(0, self.length):
            for x in range(0, self.length):
                (x2, y2) = self.matrix[x,y].getVPos()
                self.matrix[x,y].setVPos(self.restriction2(x2,y2))
                self.matrix[x,y].setToken(self.fillPlayers(x2,y2))

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

    # Moves token in position "pos" to position "newPos"
    def moveToken(self, pos, newPos):
        print("Move token")
        return True

    # Checks if player would win after moving token
    def checkWin(self):
        print("Check Win")
        return False
