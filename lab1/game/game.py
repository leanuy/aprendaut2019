### DEPENDENCIAS
### ------------------

import sys
import os

from .board import Board

def printClear():
    if os.name == 'nt':
        clear = lambda : os.system('cls')
        clear()
    else:
        clear = lambda : os.system('clear')
        clear()

### CLASE PRINCIPAL
### ------------------

class Game():

    ### METODOS PRINCIPALES
    ### -------------------

    def __init__(self):
        # Historial de tableros por turno
        self.boards = []
        self.boardPrint = 1

    # Simulación de un juego
    def play(self):

        keyboard = ''

        while keyboard != 0:

            printClear()

            b = Board()

            if self.boardPrint == 1:
                b.printBoardHex(False)
            elif self.boardPrint == 2:
                b.printBoardHex(True)
            elif self.boardPrint == 3:
                b.printBoardMatrix()

            print("-> Ingrese su jugada o el numero de la opción deseada: ")
            print("---> 1 - Ver tablero normal")
            print("---> 2 - Ver tablero grilla")
            print("---> 3 - Ver tablero matriz")
            print("---> 0 - Abandonar")
            keyboard = int(input())

            if keyboard == 1:
                self.boardPrint = 1

            elif keyboard == 2:
                self.boardPrint = 2

            elif keyboard == 3:
                self.boardPrint = 3
