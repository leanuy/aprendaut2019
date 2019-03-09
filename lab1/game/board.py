### DEPENDENCIAS
### ------------------

import numpy as np
from termcolor import colored, cprint

### CLASE PRINCIPAL
### ------------------

class Board():

 ### AUXILIAR METHODS

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

    def printSlot(self, trio):
        ((a,b), val) = trio

        print("(", end="")     
        
        if a > 0:
            cprint("+", 'red', end="")
            cprint(a, 'red', end=' ')
        elif a == 0:
            cprint("+", 'green', end="")
            cprint(a, 'green', end=' ')
        else:
            cprint(a, 'cyan', end=' ')

        if val == 0:
            print("X", end=" ")
        elif val == 1:
            cprint("O", 'yellow', end=" ")
        elif val == 2:
            cprint("O", 'magenta', end=" ")


        if b > 0:
            cprint("+", 'red', end="")
            cprint(b, 'red', end='')
        elif b == 0:
            cprint("+", 'green', end="")
            cprint(b, 'green', end='')
        else:
            cprint(b, 'cyan', end='')
        
        print(")", end="")

    def printToken(self, trio):
        ((a,b), val) = trio

        print("(", end="")     

        if val == 0:
            print("       ", end="")
        elif val == 1:
            cprint("   O   ", 'yellow', end="")
        elif val == 2:
            cprint("   O   ", 'magenta', end="")
        
        print(")", end="")

    def printBoardMatrix(self):
        for y in range(0, 9):
            for x in range(0,9):
                self.printSlot(self.matrix[x,y])

            print("")
            print("")

        print("")

    def printBoardHex(self, showGrid):

        print("")

        limit = 1
        x = 4

        for y in range(-8, 1):
            
            for s in range(0, 9 - limit):
                print("    ", end="")

            for i in range(0, limit):
                xAux = x + i
                (x2,y2) = self.inverse2(xAux,y)
                (x3,y3) = self.inverse1(x2,y2)
                
                if showGrid:
                    self.printSlot(self.matrix[x3,y3])
                else:
                    self.printToken(self.matrix[x3,y3])
            
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
                (x2,y2) = self.inverse2(xAux,y)
                (x3,y3) = self.inverse1(x2,y2)

                if showGrid:
                    self.printSlot(self.matrix[x3,y3])
                else:
                    self.printToken(self.matrix[x3,y3])
            
            print("")
            print("")

            limit = limit - 1

        print("")


    def fillPlayers(self, x, y):
        if x + y > 4:
            return 1
        elif x + y < -4:
            return 2
        return 0


    ### METODOS PRINCIPALES
    ### -------------------

    def __init__(self):
        
        self.radius = 4
        self.length = 9
        self.matrix = np.zeros((9, 9), dtype=object)

        for y in range(0, 9):
            for x in range(0,9):
                self.matrix[x,y] = (self.restriction1(x,y), 0)
                
        for y in range(0, 9):
            for x in range(0,9):
                ((x2, y2), val) = self.matrix[x,y]
                self.matrix[x,y] = (self.restriction2(x2,y2), self.fillPlayers(x2,y2))

    # Moves token in position "pos" to position "newPos"
    def moveToken(self, pos, newPos):
        print("Move token")
        return True

    # Checks if player would win after moving token
    def checkWin(self):
        print("Check Win")
        return False
